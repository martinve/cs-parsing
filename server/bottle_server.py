import __init__

import os, sys
import json
import pickle
import pprint
import uuid

import bottle
from bottle import run, template, error, static_file, request, ext, redirect

from bottle.ext import sqlalchemy
from sqlalchemy import create_engine

from models import Experiment, Sentence, Base

import logicconvert
import unified_parser
import persist


dbfile = "./data/experiments.sqlite"
protocol = "http"
port = 9002
host = "127.0.0.1"
datadir = "../data/"

engine = create_engine(f"sqlite:///{dbfile}")

app = bottle.Bottle()
plugin = sqlalchemy.Plugin(engine, Base.metadata, keyword="db", create=True, commit=True)
app.install(plugin)

init_pipeline = False


@app.get("/")
def index(db):
    rows = db.query(Experiment).order_by(Experiment.id.desc()).all()
    return template("index", rows=rows)


@app.get("/import")
def get_import():
    return template("import")


@app.route("/import", method="post")
def post_import(db):
    upfile = request.files.get("upfile")
    if not upfile:
        redirect("/import")
    if upfile.content_type != 'application/json':
        return "Only JSON files allowed"

    rawdata = upfile.file.read()  # upfile.file

    data = json.loads(rawdata)
    fmtdata = pprint.pformat(data, indent=2)

    last_id = db_persist_parse(db, data)
    redirect(f"/details/{last_id}")


@app.get("/parse")
def get_parse(db):
    return template("parse")


@app.route('/parse', method="post")
def post_parse(db):
    global init_pipeline

    passage_id = request.forms.get("passage_id")
    passage = request.forms.get("passage")

    if not passage:
        # No passage provided
        redirect("/")

    if passage_id:
        passageobj = db.query(Experiment).get(passage_id)
        passage = passageobj.passage + " " + passage

    if init_pipeline == False:
        unified_parser.init_pipeline()
        init_pipeline = True
    parse_json = unified_parser.get_passage_analysis(passage)

    # TODO: Save to passage

    fname = passage.split()[0].lower() + "-" + str(uuid.uuid4()) + ".json"
    with open(datadir + fname, 'w') as f:
        json.dump(parse_json, f, indent=2)

    last_id = persist.db_persist_parse(db, parse_json)

    logic_json = logicconvert.main(parse_json, debug=False)
    # return json.dumps()
    # return json.dumps(parse_json)

    redirect(f"/passage/{last_id}")

    return json.dumps(logic_json)


@app.get("/passage/:id")
def get_passage(id, db):
    experiment = db.query(Experiment).get(id)
    return template("details", experiment=experiment)


@app.get("/passage/:id/add")
def add_sent_to_passage(id, db):
    passage = db.query(Experiment).get(id)
    return template("parse", passage=passage)


@app.get("/sentences/:id")
def get_sentence(id, db):
    sentence = db.query(Sentence).get(id)
    return template("sentence", sentence=sentence)


@app.get("/sentence/:sentence_id/logic")
def sentence_update_logic(sentence_id, db):
    snt = db.query(Sentence).get(sentence_id)
    persist.db_update_snt_logic(db, snt)
    return redirect(f"/sentences/{sentence_id}")


@app.get('/extract')
def extract():
    print("Extracting the data.")
    return True


@app.get("/flush")
def flush(db):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    for file in os.listdir(datadir):
        if file.endswith(".json"):
            with open(datadir + file) as f:
                data = json.loads(f.read())
                persist.db_persist_parse(db, data)

    redirect("/")


@app.get("/resources")
def resources():
    return template("resources")


@app.get("/test")
def test_logic(db):
    experiments = db.query(Experiment).order_by(Experiment.id.desc()).all()
    for exp in experiments:
        for snt in exp.sentences:
            print(snt.text, snt.logic)
            if snt.logic == pickle.dumps(""):
                persist.db_update_snt_logic(db, snt)
    return "Done."


@app.route('/<filename:path>')
def serve_static(filename, path="False"):
    return static_file(filename, root='public/')


@error(404)
def error404():
    return static_file("error.html", root='./public')


if __name__ == '__main__':
    run(host=host, port=port, app=app, debug=True, reloader=True)
