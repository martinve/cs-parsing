import os, sys
import json
import math

import config
import udutil

DEBUG = config.debug_clauses

"""
Snt types are:
1: conceptual
2: fact
3: situational
"""


def snt_type_label(snt_type):
    for key, value in config.sentence_label_dict.items():
        if snt_type == value:
            return key
    return False


def get_ner(snt_ud):
    ner = {}

    # print("UD type", type(snt_ud), len(snt_ud))
    # print("UD", snt_ud)

    for tok in snt_ud:
        if tok["ner"] == "O":
            continue
        if tok["ner"][2:] in ["CARDINAL", "DATE"]:
            continue
        if tok["deprel"] in ["nmod", "nmod:poss"]:
            continue

        # print(tok["ner"], tok["lemma"])
        ner[tok["ner"]] = tok["lemma"]

    return ner


def get_articles(snt_ud):
    article_list = []
    for tok in snt_ud:
        if tok["upos"] == "DET":
            article_list.append(tok)
    return article_list


def get_upos(snt_ud, tok_type):
    ret = []
    for tok in snt_ud:
        if tok["upos"] == tok_type:
            ret.append(tok["lemma"])
    return ret


def get_xpos(snt_ud, tok_type):
    ret = []
    for tok in snt_ud:
        if tok["xpos"] == tok_type:
            ret.append(tok["lemma"])
    return ret


def get_prediction_confidence(predict):
    values = predict.values()
    nummax = sum(1 for value in predict.values() if value == max(values))
    return math.floor(10 / nummax) / 10


def get_snt_type_probabilities(snt_ud, explain=False):
    predict = {
        "sit": 0,
        "concept": 0,
        "fact": 0,
    }

    # snt ud must not be formatted
    if isinstance(snt_ud, str):
        return predict

    ner = get_ner(snt_ud)

    if ner:
        if explain: print(f"Clf: NER (sit + 10;fact +11)")
        predict["sit"] += 10
        predict["fact"] += 11
    else:
        if explain: print(f"Clf: No NER (fact -5, concept +10)")
        predict["fact"] -= 5
        predict["concept"] += 10

    def_article_count = 0
    indef_article_count = 0
    for art in get_articles(snt_ud):
        if art["lemma"] == "a":
            if explain: print(f"Clf: Indefinite article (concept +10)")
            predict["concept"] += 10
            indef_article_count += 1
            continue
        if art["lemma"] == "the" and def_article_count == 0:
            if explain: print(f"Clf: Definite article (concept -10)")
            predict["concept"] -= 5
            def_article_count += 1
            continue

    if def_article_count == 0 and indef_article_count == 0:
        if explain: print(f"Clf: No definite article (concept +10)")
        predict["concept"] += 10

    verbs = get_upos(snt_ud, "VERB")
    if verbs:
        if "have" in verbs:
            if explain: print(f"Clf: 'have' in verbs (fact +10)")
            predict["fact"] += 10
        elif "cause" in verbs:
            if explain: print(f"Clf: 'cause' in verbs (sit -10)")
            predict["sit"] -= 10
        else:
            if explain: print(f"Clf: not 'have' in verbs (sit +10)")
            predict["sit"] += 10

    aux = get_upos(snt_ud, "AUX")
    if aux:
        if "be" in aux:
            if explain: print(f"Clf: `be` in AUX (fact +10; concept +10)")
            predict["fact"] += 10
            predict["concept"] += 10

    predict["confidence"] = get_prediction_confidence(predict)

    return predict


def predict_snt_type(snt_ud, explain=False):
    if len(snt_ud) < 2:
        return 0

    if explain:
        udutil.print_plain(snt_ud)
        udutil.print_tree(snt_ud, feats=True)
        print("---")

    pred = get_snt_type_probabilities(snt_ud, explain)

    if explain:
        print(pred)

    type_label = config.sentence_label_dict[max(pred, key=pred.get)]
    return type_label


if __name__ == "__main__":

    os.system("clear")

    y_true = []
    y_pred = []

    with open("parse.json") as infile:
        data = json.load(infile)

        k = 0
        for snt in data:
            if k > 1: sys.exit(-1)

            _ud = snt['ud']
            udutil.print_sentence_tree(_ud)
            print("----")
            # print(debug_ud_parse(_ud))

            print(get_snt_type_probabilities(_ud))
            label = predict_snt_type(_ud)
            print(f"true={snt['y_true']}, predicted={label}")

            # sys.exit(-1)

            k = +1
