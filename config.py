debug_print_flag = False
debug_graph_construction = False
debug_clauses = False

server_port = 5000
server_host = "localhost"
server_uri = f"http://{server_host}:{server_port}"
cache_file = "parser_cache"
log_file = "server_log"

dummy_name = "Dummyname" # new vars start with this
question_var = "?:Q"

snt_ud = None

sentence_label_dict = {
    "concept": 1,
    "fact": 2,
    "sit": 3
}

role_dict = {
    ":arg0": "agent",
    ":arg1": "patient",
    ":arg2": "instrument",
    ":arg3": "startingPoint",
    ":arg4": "endingPoint",
    ":arg5": "modifier"
}


amr_dict = {
    ":domain": "isa",
    ":mod": "property", # "hasProperty",
    ":poss": "belongs", # "belongsTo",
    ":location": "located", # "isLocatedAt",
    "have-org-role-91": "role", # "hasRole"
    ":instrument": "with"
}