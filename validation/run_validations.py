import json
import time
import os, sys

from sklearn import metrics

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import api
import tests.sentence_heuristic_classifier as clf

ground_truth = 1

"""
Fact sentences:
- OpenbookQA:     # Total 1326 sentences

"""


def fetch_openbook_parse(filename, max_items=10):
    f = open("openbook.txt")
    row = f.readline()

    sentences = []
    k = 0
    while row:
        row = f.readline()
        if not row: continue

        row = row.strip()
        row = row.strip('"')
        row += "."
        sentences.append(row)

    passage = " ".join(sentences[:max_items])

    start = time.time()
    passage_meta = api.fetch_parse_from_server(passage)
    file = f'../data/{filename}.json'
    with open(file, 'w') as f:
        json.dump(passage_meta, f, indent=2)
        print("Saved openbook meta.")
    print(f"Fetched parse for {k} sentences in {time.time() - start}")


def validate_openbook_parse(filename):
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

    # print(y_pred)
    # print(y_true)

    # print(metrics.confusion_matrix(y_true, y_pred))
    print(metrics.classification_report(y_true, y_pred, zero_division=0))


def perform_single_prediction(filename="validate_openbook", idx=1):
    file = f'../data/{filename}.json'
    with open(file) as infile:
        data = json.load(infile)

    snt = data["sentences"][idx - 1]
    ud = snt["semparse"]["ud"][0]

    print(snt["sentence"])
    predict = clf.predict_snt_type(ud, explain=True)

    print("Predict:", predict, clf.snt_type_label(predict))


if __name__ == "__main__":

    # fetch_openbook_parse(filename="validate_openbook", max_items=100)

    if len(sys.argv) > 1:
        idx = int(sys.argv[1])
        perform_single_prediction(filename="validate_openbook", idx=idx)
    else:
        validate_openbook_parse(filename="validate_openbook")

    # Sent 3 : False 3 An example of a change in the Earth is an ocean becoming a wooded area.
    #
