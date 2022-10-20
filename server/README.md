# Parse Server

Parse server is a minimal server built on top of Bottle.py for storing and reproducing the experiment results. By default the server runs on port 9002.

To install dependencies: `pip3 install -r requirements.txt`
To run the server: `python3 bottle_server.py`
By default the server is running on `http://localhost:9002`



## Purpose And Scope

* Visualize the text-to-logic pipeline.
* Collect samples for parse results from external users.
* Visualize parse results from existing parse results.
* Reproduce the experiments for algorithm improvements.

## Data Architecture

https://nomnoml.com/#file/text-to-gk-web

## Paths

| Path | Description |
| --- | --- |
| GET /index | Display previous experiments |
| GET /parse | Enter a new passage |
| POST /parse | Parse the passage, save the JSON representation |
| GET /import | Import the previous parse |
| POST /import | Import a previous parse from previous source |
| GET /flush | Recreate the database |
| GET /passage/:id | Display passage details |
| GET /sentences/:id | Display sentence details |
| GET /sentences/:id/logic	| Update logic for a sentence |





​	
