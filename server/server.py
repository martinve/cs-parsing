import json
import os, sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from unified_parser import get_passage_analysis, init_pipeline

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import config


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):

        qs = urlparse(self.path).query
        parsed_qs = parse_qs(qs)

        passage = False
        if "passage" in parsed_qs:
            passage = parsed_qs["passage"][0]

        result = False
        if passage:
            result = get_passage_analysis(passage, "default")
            result = json.dumps(result)

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write(bytes("%s\n" % result, "utf-8"))



# ====== starting ======

if __name__ == "__main__":
    init_pipeline()

    host_name = config.server_host
    server_port = config.server_port

    webServer = HTTPServer((host_name, server_port), MyServer)
    print("Server started http://%s:%s" % (host_name, server_port))

    try:
        buffer = 1
        sys.stderr = open(config.log_file, 'w', buffer)
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

# ===== the end ======
