from flask import Flask
from flask import request

from unified_parser import get_passage_analysis, init_pipeline

app = Flask(__name__)

PORT = 5000


@app.route("/")
def parse():
    passage = request.args.get("passage", default="")
    ret = {"passage": passage}
    if passage:
        app.logger.debug(f'Parsing passage: {passage}')
        ret = get_passage_analysis(passage, "default")
    return ret


if __name__ == "__main__":
    from waitress import serve
    init_pipeline()
    serve(app, host="0.0.0.0", port=PORT)

