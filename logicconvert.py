"""
Convert a text passage to logic

"""
import json
import os
import sys
import pprint

from json_to_logic import amr_to_logic, add_question, add_question_clauses
from logger import logger
from solver import run_solver
from types_util import is_list

debug = True

load_fresh = False
save_meta = False
load_meta = True


def toggle_reload():
    global save_meta, load_meta
    if load_fresh:
        save_meta = True
        load_meta = False
    else:
        save_meta = False
        load_meta = True


def extract_meta(passage):
    import requests

    uri = "http://localhost:5000"
    json_data = None

    try:
        req = requests.get(f"{uri}/?passage={passage}")
        json_data = req.json()
    except:
        print("Cannot connect to parse server at: ", uri)
        print("Exiting.")
        sys.exit(-1)

    return json_data


def is_question(passage):
    return passage.endswith("?")


if __name__ == "__main__":

    # os.system("clear")

    if len(sys.argv) < 2:
        print("No input provided")
        sys.exit()

    passage = sys.argv[1]

    if "--refresh" in sys.argv:
        load_fresh = True

    if "--clear" in sys.argv:
        os.system("clear")

    toggle_reload()

    question = False
    if len(sys.argv) == 3:
        question_str = sys.argv[2]

    if load_meta:
        with open('data/passage_meta.json') as f:
            passage_meta = json.load(f)
    else:
        passage_meta = extract_meta(passage)

    if save_meta:
        with open('data/passage_meta.json', 'w') as f:
            json.dump(passage_meta, f, indent=2)
            logger.info("Saved passage meta.")

    logic = []
    question = None

    for sent in passage_meta['sentences']:
        amr = sent["semparse"]["amr"]
        const = sent["constituency"]

        clauses = amr_to_logic(amr, const)

        if debug:
            c = pprint.pformat(clauses, indent=2, compact=False)
            logger.debug(f"Snt: {sent['sentence']}, ques={is_question(sent['sentence'])}")
            logger.debug(f"Const: {sent['constituency']}")
            logger.debug(f"AMR: {amr}")
            logger.debug(f"Clauses: ({len(clauses)}) \n{c}")

        if not is_question(sent["sentence"]):
            for k, cl in enumerate(clauses):
                clauses[k] = {"@logic": cl}
            logic.extend(clauses)
        else:
            logger.error(f"Question: {c}")
            question = amr_to_logic(amr, const)

    # If we use parsed clauses as a
    if is_list(question):
        logger.info("Assign question clauses.")
        logic = add_question_clauses(logic, question)
    # elif question_str and 1 == 0:
    #     logger.info("Assign question.")
    #     logic = add_question_clauses(logic, question_str)

    run_solver(logic, print_logic=True)
