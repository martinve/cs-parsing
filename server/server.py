import sys
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote

try:
    import stanza  # the only non-standard library dependency
except:
    print("""nlpserver needs stanza: to install stanza, do
pip install stanza
python -c 'import stanza; stanza.download("en")'""")
    sys.exit(0)

# see https://stanfordnlp.github.io/stanza/
# to install stanza, do
#  pip install stanza
#  python -c 'import stanza; stanza.download("en")'

# ======= configuration globals ======

host_name = "localhost"
server_port = 5000
logfile = "/dev/null"  # here server logs the requests

# ====== globals used during work ========

nlp = None  # at startup nlp is assigned the stanza pipeline


# === request processing ===

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        text = unquote(self.path)  # urldecode
        if text: text = text[1:]  # remove initial slash
        result = parse_text(text)  # call stanza parser
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write(bytes("%s\n" % result, "utf-8"))


def parse_text(text):
    global nlp
    doc = nlp(text)
    docpy = doc.to_dict()
    entities = []
    for el in doc.entities:
        entities.append(el.to_dict())
    wrapper = {"doc": docpy, "entities": entities}
    resjson = json.dumps(wrapper)
    return resjson


# ====== starting ======

if __name__ == "__main__":
    print("Starting to build the stanza pipeline.")
    nlp = stanza.Pipeline(lang='en', processors='tokenize,ner,pos,lemma,depparse')
    webServer = HTTPServer((host_name, server_port), MyServer)
    print("Server started http://%s:%s" % (host_name, server_port))

    try:
        buffer = 1
        sys.stderr = open(logfile, 'w', buffer)
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

# ===== the end ======
