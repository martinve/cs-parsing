import json
import sys, os
import subprocess
import warnings
import amrlib
import textacy
import time


from logger import logger

import stanza
import benepar
import spacy

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from debugger import debug_print


warnings.filterwarnings('ignore')
os.environ['TOKENIZERS_PARALLELISM'] = 'true'

dirname = os.path.dirname(__file__)

# model_stog_dir = os.path.join(dirname, "models/model_parse_xfm_bart_base-v0_1_0")
model_stog_dir = os.path.join(dirname, "models/model_stog")

model_gtos_dir = os.path.join(dirname, "models/model_gtos")

stanza_nlp = None
nlp = None

debug = False


def init_pipeline():
    global stanza_nlp, nlp

    debug_print("Initializing model pipeline.")

    amrlib.load_stog_model(model_dir=model_stog_dir)
    # gtos = amrlib.load_gtos_model(model_dir=model_gtos_dir)
    amrlib.setup_spacy_extension()

    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe('benepar', config={'model': 'benepar_en3'})
    stanza_nlp = stanza.Pipeline(lang='en', processors='tokenize,ner,pos,lemma,constituency,depparse')



def udparse(text):
    start = time.time()

    if stanza_nlp is None:
        init_pipeline()

    doc = stanza_nlp(text)
    docpy = doc.to_dict()
    debug_print("[Parse 1] UD in:", time.time() - start)
    return docpy


def get_ud_tokens(sent_ud):
    if not sent_ud:
        return []
    return sent_ud[0]


def get_word_types(sent_ud):
    wordtypes = {}
    for token in get_ud_tokens(sent_ud):
        pos = token["upos"]
        if pos in ["DET", "PUNCT"]:
            continue
        if pos not in wordtypes.keys():
            wordtypes[pos] = []
        wordtypes[pos].append(token["text"])
    return wordtypes


def get_named_entities(sent_ud):
    ner = {}
    current_label = None
    current_tokens = []

    def flush_entity():
        nonlocal current_label, current_tokens
        if current_label and current_tokens:
            if current_label not in ner.keys():
                ner[current_label] = []
            ner[current_label].append(" ".join(current_tokens))
        current_label = None
        current_tokens = []

    for token in get_ud_tokens(sent_ud):
        token_ner = token.get("ner") or "O"
        if token_ner == "O":
            flush_entity()
            continue

        prefix, label = token_ner.split("-", 1)
        if prefix == "S":
            flush_entity()
            ner.setdefault(label, []).append(token["text"])
        elif prefix == "B":
            flush_entity()
            current_label = label
            current_tokens = [token["text"]]
        elif prefix in ["I", "E"] and current_label == label:
            current_tokens.append(token["text"])
            if prefix == "E":
                flush_entity()
        else:
            flush_entity()

    flush_entity()
    return ner


def get_wordnet_hierarchy(sent):
    start = time.time()

    wordnet = []
    cmd = "python3 wordnet_tree.py -s"

    wordnet_types = {
        "VERB": "v",
        "NOUN": "n"
    }

    for token in sent:
        if token.pos_ not in wordnet_types.keys():
            continue
        syn = ".".join([token.lemma_, wordnet_types[token.pos_], "01"])
        # debug_print(token, syn, sep=" -> ")

        outp = subprocess.run(cmd + " " + syn, stdout=subprocess.PIPE, shell=True)
        res = str(outp.stdout, 'utf-8')
        parents = [x.strip() for x in list(filter(None, res.split("\n")))]
        parents.reverse()

        word = {"word": token.text, "syn": syn, "parents": parents}

        wordnet.append(word)

    if debug:
        debug_print("[Onto] Wordnet:", time.time() - start)

    return wordnet


def get_noun_phrases(sent_ud):
    chunks = []
    tokens = get_ud_tokens(sent_ud)
    token_by_id = {token["id"]: token for token in tokens}
    nominal_pos = {"NOUN", "PROPN", "PRON"}
    modifier_deps = {"det", "amod", "compound", "flat", "fixed", "nummod", "nmod:poss"}

    for token in tokens:
        if token["upos"] not in nominal_pos:
            continue

        phrase_token_ids = [token["id"]]
        phrase_token_ids.extend(
            child["id"]
            for child in tokens
            if child.get("head") == token["id"] and child.get("deprel") in modifier_deps
        )
        phrase = " ".join(token_by_id[token_id]["text"] for token_id in sorted(phrase_token_ids))
        chunks.append(phrase)

    return chunks


def get_constituency(sent):
    start = time.time()
    constituency = sent._.parse_string
    debug_print("[Parse 2] Constituency in:", time.time() - start)
    return constituency


def get_verb_phrases(sent_ud):
    chunks = []
    tokens = get_ud_tokens(sent_ud)
    token_by_id = {token["id"]: token for token in tokens}
    modifier_deps = {"aux", "advmod", "compound:prt"}

    for token in tokens:
        if token["upos"] != "VERB":
            continue

        phrase_token_ids = [token["id"]]
        phrase_token_ids.extend(
            child["id"]
            for child in tokens
            if child.get("head") == token["id"] and child.get("deprel") in modifier_deps
        )
        phrase = " ".join(token_by_id[token_id]["text"] for token_id in sorted(phrase_token_ids))
        chunks.append(phrase)
    return chunks


def get_svo_triples(sent):
    triples = textacy.extract.triples.subject_verb_object_triples(sent)
    svo = []
    for t in triples:
        item = {
            "s": '_'.join([str(x) for x in t.subject]),
            "v": '_'.join([str(x) for x in t.verb]),
            "o": '_'.join([str(x) for x in t.object])
        }
        svo.append(item)
    return svo


def format_clause(txt):
    """
    Remove AMR specific clause modifiers, e.g :ARG0 is transformed to ARG0
    """
    return txt.replace(":", "")


def format_constant(txt):
    """
    Constants are lowercase
    """
    ret = txt.lower().strip('"')
    return ret


def format_variable(txt):
    """
    Variables are uppercase
    """
    return txt.upper()


def get_sentence_analysis(sent: object):
    """
    :type sent: spacy.tokens.span.Span
    """
    if len(sent.text.strip()) < 1:
        return False

    # debug_print("Sent typr", type(sent))

    sent_ud = udparse(sent.text)

    constituency = str(get_constituency(sent))

    # start = time.time()
    # svo_triples = get_svo_triples(sent)
    # debug_print("[Parse 3] triples in:", time.time() - start)

    parsed: dict[str, object] = {
        "sentence": sent.text,
        "wordtypes": get_word_types(sent_ud),
        "ner": get_named_entities(sent_ud),
        # "wordnet": get_wordnet_hierarchy(sent),
        "syntaxparse": {
            "verbphrase": get_verb_phrases(sent_ud),
            "nounphrase": get_noun_phrases(sent_ud)
        },
        "semparse": {
            "amr": get_amr_parse(sent),
            "ud": sent_ud
        },
        # "triples": svo_triples,
        "constituency": constituency,
        # "logic": str(generate_clauses(cleanup_tree(sent._.to_amr()[0])))
    }

    return parsed


def get_amr_sentence(sent):
    text = sent.text.strip()
    if not text or text[-1] in ".!?":
        return sent

    doc = nlp(text + ".")
    return next(doc.sents)


def get_amr_parse(sent):
    start = time.time()
    parse = get_amr_sentence(sent)._.to_amr()[0]
    if debug:
        debug_print("[Parse 0] AMR in:", time.time() - start)
    return parse


def get_passage_analysis(passage: str, context=False):
    st0 = time.time()

    if nlp is None:
        init_pipeline()

    doc = textacy.make_spacy_doc(passage, lang=nlp)
    debug_print("textacy.make_spacy_doc in:", time.time() - st0)

    # debug_print("DOC", type(doc))

    # meta = {"passage": passage, "context": context, "sentences": [], "spacy": doc.to_json()}
    meta = {"passage": passage, "context": context, "sentences": []}

    k = 0
    for sent in doc.sents:
        start = time.time()
        parsed = get_sentence_analysis(sent)
        end = time.time()
        debug_print(k, "get_sentence_analysis:", time.time() - start)

        if not parsed:
            continue

        meta["sentences"].append(parsed)
        k = k + 1

    return meta


if __name__ == "__main__":

    if len(sys.argv) == 1:
        debug_print("No input passage provided")
        sys.exit()

    passage_in = sys.argv[1]

    init_pipeline()

    passage_meta = get_passage_analysis(passage_in, "default")
    debug_print(json.dumps(passage_meta, indent=2))
