import os

_server_dir = os.path.dirname(os.path.abspath(__file__))
dbfile = os.path.join(_server_dir, "cache", "experiments.sqlite")
protocol = "http"
port = 9010
host = "127.0.0.1"
datadir = os.path.join(_server_dir, "cache") + os.sep

debug_clauses = False
