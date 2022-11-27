import json
import time
import os, sys

from sklearn import metrics

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import api
import tests.sentence_heuristic_classifier as clf


snt_types = {
    "concept": 1,
    "fact": 2,
    "sit": 3
}

sources = {
    "openbook": 1,
    "dbpedia": 2,
    "socialiqa": 3
}



"""
Fact sentences:
- OpenbookQA:     # Total 1326 sentences

"""





def fetch_corpus_parse(in_filename, out_filename, max_items=10):
    f = open(in_filename)
    row = f.readline()

    sentences = []
    k = 0
    while row:
        row = f.readline()
        if not row: continue

        row = row.strip()
        row = row.strip('"')
        if row[-1] not in ["."]:
            row += "."
        sentences.append(row)

    passage = " ".join(sentences[:max_items])

    start = time.time()
    passage_meta = api.fetch_parse_from_server(passage)
    file = f'../data/{out_filename}.json'
    with open(file, 'w') as f:
        json.dump(passage_meta, f, indent=2)
        print("Saved openbook meta.")
    print(f"Fetched parse for {k} sentences in {time.time() - start}")


def validate_openbook_parse(filename, ground_truth=1):
    y_true = []
    y_pred = []

    file = f'../data/{filename}.json'
    with open(file) as infile:
        data = json.load(infile)

        k = 1
        errored = 0
        for sent in data["sentences"]:
            ud = sent["semparse"]["ud"][0]

            predict = clf.predict_snt_type(ud)

            if predict != ground_truth:
                errored += 1
                print("Sent ", k, ": ", predict == ground_truth, " (", clf.snt_type_label(predict), ") ", sent["sentence"], sep="")

            # if predict != ground_truth: print(sent["sentence"])

            y_true.append(ground_truth)
            y_pred.append(predict)

            k += 1

    print("Total errored:", errored)
    print("Total sentences", k - 1)

    # print(y_pred)
    # print(y_true)

    # print(metrics.confusion_matrix(y_true, y_pred))
    print(metrics.classification_report(y_true, y_pred, zero_division=0))


def perform_single_prediction(name, ground_truth=1, idx=1):
    filename = f"validate_{name}"
    file = f'../data/{filename}.json'
    with open(file) as infile:
        data = json.load(infile)

    snt = data["sentences"][idx - 1]
    ud = snt["semparse"]["ud"][0]

    print(snt["sentence"])
    predict = clf.predict_snt_type(ud, explain=True)

    print("Predict:", predict, clf.snt_type_label(predict))


def prepare(kb_list):
    for item in kb_list:
        if item == "openbook":
            print("Preparing OpenbookQA Data")
            fetch_corpus_parse("openbook.txt", out_filename="validate_openbook", max_items=100)
        if item  == "winograd":
            print("Preparing Winograd Schema Data")
            fetch_corpus_parse("winograd.txt", out_filename="validate_winograd", max_items=100)
        if item == "dbpedia":
            print("Preparing DBPedia Schema Data")
            fetch_corpus_parse("dbpedia.txt", out_filename="validate_dbpedia", max_items=100)
        if item == "socialiqa":
            print("Preparing Social IQA Data")
            fetch_corpus_parse("socialiqa.txt", out_filename="validate_socialiqa", max_items=100)



def validate(name, gold_label):
    filename = f"validate_{name}"
    validate_openbook_parse(filename, gold_label)


if __name__ == "__main__":

    # prepare(["dbpedia"])

    # sources = ["openbook", "socialiqa", "dbpedia]
    name = None
    if len(sys.argv) > 1:
        name = sys.argv[1]
    if name not in sources.keys():
        name = list(sources.keys())[0]


    truth = sources[name]

    if len(sys.argv) > 2:
        idx = int(sys.argv[2])
        perform_single_prediction(name, truth, idx=idx)
    else:
        validate(name, truth)



