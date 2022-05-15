from flask import Flask
from flask import request
from waitress import serve
import os, sys
from unified_parser import get_passage_analysis, init_pipeline

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import config

app = Flask(__name__)


@app.route("/")
def parse():
    passage = request.args.get("passage", default="")
    ret = {"passage": passage}
    if passage:
        app.logger.debug(f'Parsing passage: {passage}')
        ret = get_passage_analysis(passage, "default")
    return ret


if __name__ == "__main__":
    init_pipeline()
    serve(app, host="0.0.0.0", port=config.server_port)
