# CS-Parser

CS-Parser is an experimental English text-to-logic system.  It turns a passage
into linguistic annotations and Abstract Meaning Representation (AMR), then
converts an AMR graph into clauses that can be inspected in a Bottle web UI or
passed to the bundled `gk` prover.  Its target representation is compatible
with the [JSON-LD-Logic](https://github.com/tammet/json-ld-logic) style: the
legacy pipeline emits clauses wrapped as `{"@logic": [...]}`.

This repository is research code, rather than a packaged library.  In
particular, model files are intentionally not committed and the web UI and the
legacy command-line client have different configuration and output paths.  The
sections below describe the code as it currently works, including those
boundaries.

## System overview

```
English passage
      |
      v
server/unified_parser.py
  spaCy + Stanza + Benepar + AMRLib
      |
      +--> sentence metadata (NER, POS groups, noun/verb phrases,
      |    constituency tree, Universal Dependencies)
      |
      v
AMR PENMAN graph
      |
      +------------------------------+
      |                              |
      v                              v
amr_clausifier.py              amr_to_json.py -> json_to_logic.py
(UI clausifier)                (legacy nested-list converter)
      |                              |
      v                              v
web UI sentence logic          JSON-LD-Logic-style clauses
                                     |
                                     v
                                RoleReplacer / simplifier
                                     |
                                     v
                                solver/gk (optional)
```

### Parsing and stored data

`server/unified_parser.py` owns the NLP pipeline.  AMRLib supplies a
sentence-to-graph model; a spaCy pipeline backed by Stanza supplies tokenisation,
named entities, POS tags, lemmata, constituency parsing and dependency parsing.
For every detected sentence, `get_passage_analysis()` returns a structure like:

```json
{
  "passage": "Brutus stabs Caesar with a knife.",
  "context": false,
  "sentences": [{
    "sentence": "Brutus stabs Caesar with a knife.",
    "wordtypes": {"PROPN": ["Brutus", "Caesar"], "VERB": ["stabs"]},
    "ner": {"PERSON": ["Brutus", "Caesar"]},
    "syntaxparse": {"verbphrase": ["stabs"], "nounphrase": ["Brutus", "Caesar", "a knife"]},
    "semparse": {"amr": "(… PENMAN AMR …)", "ud": [["… UD token records …"]]},
    "constituency": "(S …)"
  }]
}
```

The exact values depend on the installed NLP model.  `server/persist.py`
serializes that result into SQLite `passages` and `sentences` records.  A parse
is persisted first; logic is generated separately when the user opens the
sentence logic route.

### AMR-to-logic conversion

There are two implementations:

| Component | Used by | What it does |
| --- | --- | --- |
| `amr_clausifier.py` | Web UI (`/sentences/:id/logic`) | Decodes PENMAN with `penman`, replaces applicable PropBank and AMR roles, and returns a list of relation clauses. |
| `amr_to_json.py` + `json_to_logic.py` | `logicconvert.py` | Transforms AMR text into a nested list, walks the tree, normalizes case, and creates JSON-LD-Logic-style clauses. |
| `RoleReplacer.py` | Legacy pipeline | Rewrites roles such as `:ARG0` and `:ARG1` to `agent` and `patient`; also maps selected AMR relations such as `:domain` to `isa`. |
| `simplifier.py` | Legacy pipeline | Placeholder simplifier; it currently mainly adjusts conjunction/disjunction handling and logs that it is incomplete. |

The mapping tables are in `config.py`.  The legacy path applies them through
`RoleReplacer` after `json_to_logic` has lowercased its clauses. They are
deliberately small, so an unmapped AMR relation is retained rather than
inferred. Question handling in the legacy converter is incomplete: a sentence
ending in `?` reaches `question_from_amr()`, which currently returns an empty
list.

### Sentence classification and proof

Before role replacement, the legacy pipeline applies the heuristic classifier
in `classifier/sentence_heuristic_classifier.py`.  It labels a sentence as
`concept`, `fact`, or `sit` using UD features such as named entities, articles,
verbs and auxiliary verbs.  The label is stored in the per-sentence context and
is available to later simplification.

`solver.py` can write a logic program to `solver/gk_in.js` and execute the
bundled `solver/gk` binary.  It returns `True`, `False`, or `None` depending on
the prover response.  Running it overwrites `solver/gk_in.js`.

## Examples

### 1. Inspect the legacy AMR reader without NLP models

`amr_to_json.py` is the only conversion stage that has no third-party Python
dependency. It is useful for inspecting the intermediate nested-list form,
although it is a legacy, text-rewriting parser rather than a general PENMAN
reader:

```bash
python - <<'PY'
from amr_to_json import amr_to_json

amr = '''(s / stab-01
  :ARG0 (p / person)
  :ARG1 (c / person))'''

print(amr_to_json(amr))
PY
```

For the bundled test inputs, the reader produced a non-empty graph for 17 of
21 cases; see [EXPERIMENTS.md](EXPERIMENTS.md) for the known unsupported
forms. Treat the resulting list as an intermediate representation, not the
final logic API.

### 2. Convert a known AMR graph with the Penman utility

This exercises `amrutil.generate_clauses()`. It requires `penman` and, because
that module imports formatting helpers from `server/unified_parser.py`, the
parser runtime dependencies must also be importable. It does not load the NLP
models or call `init_pipeline()`.

```bash
python - <<'PY'
from amrutil import generate_clauses

amr = '''(s / stab-01
  :ARG0 (p / person :name (n / name :op1 "Brutus"))
  :ARG1 (c / person :name (n2 / name :op1 "Caesar"))
  :instrument (k / knife))'''

print(generate_clauses(amr))
PY
```

The result is a JSON array of concept and relation clauses. The utility's
current direct role lookup compares the colon-stripped AMR role (for example,
`ARG0`) with colon-prefixed mapping keys, so it currently retains `ARG0` and
`ARG1`; the legacy pipeline below performs the configured `agent` and
`patient` rewrites. The exact set of concept clauses also reflects AMR node
arity and name attributes.

The repository includes more AMR inputs in `amr_test_cases.py`; they are useful
for checking names, conjunctions, negation, quantities, comparison and roles.

### 3. Run the full parser in Python

After installing the models expected by `server/unified_parser.py`, parse text
directly without the UI:

```bash
python - <<'PY'
import json
from server import unified_parser

unified_parser.init_pipeline()       # expensive; call once per process
result = unified_parser.get_passage_analysis(
    "Brutus stabs Caesar with a knife. Caesar falls."
)

for sentence in result["sentences"]:
    print(sentence["sentence"])
    print(sentence["semparse"]["amr"])

with open("parse-result.json", "w") as output:
    json.dump(result, output, indent=2)
PY
```

`init_pipeline()` loads AMRLib's sentence-to-graph model from
`server/models/model_stog`, then creates the spaCy/Stanza/Benepar pipelines.
Expect the first call to take considerably longer than later calls.

### 4. Generate legacy JSON-LD-Logic clauses from parsed metadata

The legacy converter consumes one item from `result["sentences"]`, not raw
text.  It can be used after example 2 as follows:

```python
from logicconvert import get_sentence_clauses

clauses, context = get_sentence_clauses(
    result["sentences"][0], idx=0, debug=False, ud_shift=True
)
print(context["type"])
print(clauses)
# Example shape: {"@logic": ["agent", "stab.01", "person0"]}
```

Variables in non-question clauses receive the sentence index suffix, which
keeps variables from separate sentences distinct.  The clause values depend on
the AMR model's graph, so the example shape is illustrative rather than a
fixed expected output.

## Setup and intended web workflow

Use the project NLP environment, then install both dependency manifests as
needed. The commands below assume the environment is located at
`~/Code/env/nlp`.
`penman` is declared in `server/requirements.txt`; install it explicitly if
you want to use the root-level Penman utilities without installing the server
requirements:

```bash
source ~/Code/env/nlp/bin/activate
python -m pip install -r requirements.txt
python -m pip install -r server/requirements.txt sqlalchemy
mkdir -p cache server/cache
```

The parser additionally needs:

* an AMRLib sentence-to-graph model at `server/models/model_stog`;
* Stanza English resources and the spaCy English model;
* the Benepar model named `benepar_en3` (the model selected in
  `unified_parser.py`).

`server/install_models.sh` shows the intended AMR model download and symlink;
review it before running it.  `server/download_models.py` downloads some NLP
resources but currently asks Benepar for `benepar_cen3`, while the parser loads
`benepar_en3`, so install the latter explicitly or update that helper.

When the server dependencies and models are ready, its intended entry point is:

```bash
cd server
python run_server.py
```

`server/settings.py` defaults to `http://127.0.0.1:9010`; submitting the
`/parse` form performs parsing, writes a JSON cache file under `cache/` (the
path is `../cache/` relative to `server/`), persists the passage in SQLite at
`server/cache/experiments.sqlite`, and redirects to its passage page. From
there, opening a sentence's logic page invokes the clausifier. Neither cache
directory is created by the application, hence the setup command above.

## Current integration notes

These items are useful when reproducing or extending the system:

* The old root README referred to `config.php` and `bottle_server.py`; neither
  is an active file.  The actual server configuration is `server/settings.py`
  and the entry point is `server/run_server.py`.
* `server/run_server.py` imports `static_controller`, but that module is not
  present in this checkout.  Add or remove that import before expecting the web
  server to start.
* `amr_clausifier.py` imports `amrtest_config`, which is also absent from this
  checkout.  Thus the UI's current sentence-logic route cannot load its
  intended clausifier without that configuration module. Example 2 uses
  `amrutil.generate_clauses()` so it remains runnable once `penman` is
  installed.
* `logicconvert.py --reload` calls `api.fetch_parse_from_server()`. That helper
  does return its decoded response, but it posts to `/parse`, whose successful
  response is an HTML redirect rather than JSON. Its default port in root
  `config.py` (`10001`) also differs from the web server's default (`9010`).
  Use the direct Python interfaces above, or reconcile the endpoint contract
  and settings, before using that client path.
* `server/start.sh` still invokes `server.py`, which is not included; use
  `run_server.py` instead.

## Repository guide

| Path | Responsibility |
| --- | --- |
| `server/unified_parser.py` | NLP and AMR model orchestration; produces passage metadata. |
| `server/run_server.py` and `server/*_controller.py` | Bottle routes, templates and persistence-backed UI. |
| `amr_clausifier.py` | PENMAN/AMR to normalized clauses for the UI. |
| `logicconvert.py`, `amr_to_json.py`, `json_to_logic.py` | Legacy AMR-to-JSON-LD-Logic pipeline. |
| `RoleReplacer.py`, `simplifier.py`, `config.py` | Predicate mappings, sentence context and post-processing rules. |
| `solver.py`, `solver/gk` | Optional interface to the GK logical prover. |
| `datasets/` | bAbI-style task datasets used for experimentation. |
