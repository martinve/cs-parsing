import config
import requests
import sys
import time


def fetch_parse_from_server(input_text):

    json_data = None
    try:
        start = time.time()
        req = requests.get(f"{config.server_uri}/?passage={input_text}")
        json_data = req.json()
    except Exception as e:
        print("Cannot connect to parse server at: ", config.server_uri)
        print(e)
        print("Exiting.")
        sys.exit(-1)

    end = time.time()
    print("Results fetched in:", end - start)
    # sys.exit(-1)

    return json_data