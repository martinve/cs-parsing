from flask import Flask
from flask import request
from unified_parser import extract_meta

app = Flask(__name__)

@app.route("/")
def parse():
    passage = request.args.get("passage", default="")
    ret = {"passage": passage}

    if passage:
        app.logger.debug(f'Parsing passage: {passage}')
        ret = extract_meta(passage, "default", "__main__")

    return ret


if __name__ == "__main__":
    app.run(port=5000, debug=False)
