import pickle
from bottle import redirect
from models import Experiment, Sentence
import amrutil
import logicconvert


def db_persist_parse(db, data):
    passage = data["passage"]
    p2 = passage

    exists = db.query(Experiment).filter(Experiment.passage == passage).first()
    if 1 == 0 and exists:
        redirect("/")  # Passage already exists

    exp = Experiment()
    exp.passage = passage
    exp.rawdata = pickle.dumps(data)
    exp.context = ""

    for snt in data["sentences"]:
        text = snt["sentence"]
        parse_amr = snt["semparse"]["amr"]
        udraw = snt["semparse"]["ud"]
        parse_ud = pickle.dumps(udraw)

        try:
            logic = snt["logic"]["json"]
        except KeyError:
            logic = ""

        rawvalue = pickle.dumps(snt)
        parse_ud_raw = pickle.dumps(udraw)

        snt = Sentence()
        snt.text = text
        snt.parse_amr = parse_amr
        snt.parse_ud = parse_ud
        snt.parse_ud_raw = ""
        snt.context = ""
        snt.rawvalue = pickle.dumps(rawvalue)
        snt.logic = pickle.dumps(logic)

        exp.sentences.append(snt)

    db.add(exp)
    db.commit()

    return exp.id


def db_update_snt_logic(db, snt):
    sntobj = {
        "sentence": snt.text,
        "semparse": {
            "amr": snt.parse_amr,
            "ud": pickle.loads(snt.parse_ud)
        }
    }
    logic, context = logicconvert.get_sentnence_clauses(sntobj, 0, ud_shift=True, debug=False, json_ld_logic=False)
    simpl_logic = amrutil.get_simplified_logic(snt.parse_amr)

    snt.logic = pickle.dumps(logic)
    snt.context = pickle.dumps(context)
    snt.simpl_logic = pickle.dumps(simpl_logic)
    db.commit()
