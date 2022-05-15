import csv
import json
import re
import sys

from sklearn import metrics

from amr_to_json import amr_to_json
from logger import logger
from logicconvert import fetch_parse_from_server
from tests.sentence_heuristic_classifier import predict_snt_type
from tests.test_ud_parse import get_list_word
from types_util import is_verb

"""
Given a sentence, predict the type of sentence:

1 **Conceptual statements** like "Cats are animals", "Animals have two legs", which do not describe a specific situation and are not dependent on uncommon circumstances. Typically they describe concepts.

2 **Fact statements** like "Mozart was a composer", "Tallinn is a capital of Estonia", which describe named entities, again, not dependent on uncommon circumstances.

3. **Situational statements**, which describe a concrete situation and events happening with/in this situation, like "A cat was catching mice", "Mozart sat down and started playing a piano".

"""

snt_types = {
    1: "conceptual",
    2: "fact",
    3: "situational"
}


def constituency_to_json(parse):
    p = parse.replace("(", "[")
    p = p.replace(")", "]")
    p = p.replace(") (", "],[")
    p = re.sub(r'([a-zA-Z]+)', r'"\1"', p)
    # p=re.subn("([a-z]*)","*",p, count=1000, flags=0)
    p = p.replace(" ", ",")
    p = p.replace(".,.", "\".\",\".\"")
    p = p.replace(", ,", "\",\",\",\"")
    p = p.replace("[,,,]", "[\",\",\",\"]")

    tree = json.loads(p)
    return tree


def get_list_el(lst, tag):
    """
    get_list_el(tree, "ADVP")
    """
    if not lst: return None
    i = 0
    while i < len(lst):
        el = lst[i]
        if type(el) == list:
            if el[0] == tag:
                return el
        i += 1
    return None


def predict_snt_type_(amr_lst, ud_lst):
    amr_root = amr_lst[0][1]

    if is_verb(amr_root):
        amr_root = amr_root.split("-")[0]

    ud_root = get_list_word(ud_lst, amr_root)

    snt_type = 0

    if not ud_root:
        logger.warning(f"Cannot get UD root for {amr_root}")
        logger.warning(ud_lst)
    else:
        if ud_root["upos"] == "NOUN":
            snt_type = 1
        elif ud_root["upos"] == "VERB":
            snt_type = 3

    logger.warning(f"Roots: amr={amr_root}, ud={ud_root}")

    # pprint(amr_lst, indent=2)
    # print("D0", get_list_el(ud_lst, "VP"))
    # print("D1", get_list_elword(ud_lst, "VP"))
    # print("D2", get_list_word(ud_lst, "animals"))

    # pprint(ud_lst, indent=2)

    return snt_type


def parse_sentences():
    parse = []
    y_true = []
    y_pred = []

    with open("sentence_classifier_data.csv") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:

            if not row: continue

            print("row", row)
            label = int(row[0])
            sent = row[1]

            meta = fetch_parse_from_server(sent)["sentences"][0]

            amr = meta["semparse"]["amr"]
            const = meta["constituency"]
            ud = meta["semparse"]["ud"][0]

            # logger.debug(f"UD:{ud}\nAMR:{amr}")
            # logger.info(meta)

            amr_lst = amr_to_json(amr)
            ud_lst = ud

            # pprint(ud_lst, indent=2)

            predicted_label = predict_snt_type(ud_lst)

            y_true.append(label)
            y_pred.append(predicted_label)

            logger.info(f"y_true={label}, y_pred={predicted_label}, sent={sent}")

            # assert predicted_label == label

            # sys.exit(-1)
            parse.append({
                "y_true": label,
                "snt": sent,
                "amr": amr,
                "ud": ud,
                "constituency": const
            })

        with open('parse.json', 'w') as f:
            json.dump(parse, f, indent=2)
            logger.info("Saved passage meta.")

        return y_pred, y_true


def get_ud_root(snt):
    for tok in snt:
        if tok["deprel"] == "root":
            return tok


if __name__ == "__main__":

    y_pred, y_true = parse_sentences()
    print(y_pred, y_true)

    print(metrics.confusion_matrix(y_true, y_pred))
    print(metrics.classification_report(y_true, y_pred))

    sys.exit(-1)

    y_true = []
    y_pred = []

    with open("parse.json") as infile:
        data = json.load(infile)

        for snt in data:
            amr_lst = amr_to_json(snt["amr"])
            ud_lst = snt["ud"]
            constituency = snt["constituency"]
            uroot = get_ud_root(ud_lst)

            print(f"S:{snt['snt']} label={snt['label']}")
            print("A:", amr_lst)
            print("C:", constituency)
            debug_print_sentence_tree(snt["ud"])
            # print("U:", ud_lst)
            print("UROOT:", uroot)
            print("---")

            predicted_label = predict_snt_type(amr_lst, ud_lst)

            y_true.append(snt["label"])
            y_pred.append(predicted_label)


