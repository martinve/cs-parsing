import json
import re
import sys, os
import subprocess
import warnings
import amrlib
import penman
import textacy
import benepar

from logger import logger

warnings.filterwarnings('ignore')

# spacy.cli.download("en_core_web_sm")
# benepar.download('benepar_en3', quiet=True)

os.environ['TOKENIZERS_PARALLELISM'] = 'true'

dirname = os.path.dirname(__file__)
model_stog_dir = os.path.join(dirname, "models/model_stog")

stog = amrlib.load_stog_model(model_dir=model_stog_dir)

amrlib.setup_spacy_extension()

# Constituency parsing
en = textacy.load_spacy_lang("en_core_web_sm")
en.add_pipe('benepar', config={'model': 'benepar_en3'})

# TODO: Add lemmatizer to Berkley Neural Parser pipeline

role_dict = {
    "ARG0": "agent",
    "ARG1": "patient",
    "ARG2": "instrument",
    "ARG3": "startingPoint",
    "ARG4": "endingPoint",
    "ARGN": "modifier"
}


def get_word_types(sent):
    print("SENT TYPE:", type(sent))

    wordtypes = {}
    for token in sent:
        if token.pos_ in ["DET", "PUNCT"]:
            continue
        if token.pos_ not in wordtypes.keys():
            wordtypes[token.pos_] = []
        wordtypes[token.pos_].append(token.text)
    return wordtypes


def get_named_entities(sent):
    ner = {}
    for ent in sent.ents:
        if ent.label_ not in ner.keys():
            ner[ent.label_] = []
        ner[ent.label_].append(ent.text)
    return ner


def get_wordnet_hierarchy(sent):
    wordnet = []
    cmd = "python3 ./wordnet_tree/wordnet_tree.py -s"

    wordnet_types = {
        "VERB": "v",
        "NOUN": "n"
    }

    for token in sent:
        if token.pos_ not in wordnet_types.keys():
            continue
        syn = ".".join([token.lemma_, wordnet_types[token.pos_], "01"])
        # print(token, syn, sep=" -> ")

        outp = subprocess.run(cmd + " " + syn, stdout=subprocess.PIPE, shell=True)
        res = str(outp.stdout, 'utf-8')
        parents = [x.strip() for x in list(filter(None, res.split("\n")))]
        parents.reverse()

        word = {"word": token.text, "syn": syn, "parents": parents}

        wordnet.append(word)
    return wordnet


def get_noun_phrases(sent):
    chunks = []
    for np in sent.noun_chunks:
        chunks.append(np.text)
    return chunks


def analyze_sentence(sent, out):
    if len(sent.text.strip()) < 1:
        return False

    parsed: dict[str, object] = {"sentence": sent.text}

    wordtypes = get_word_types(sent)
    parsed["wordtypes"] = wordtypes

    ner = get_named_entities(sent)
    parsed["ner"] = ner

    wordnet = get_wordnet_hierarchy(sent)
    parsed["wordnet"] = wordnet

    parsed["syntaxparse"] = {
        "verbphrase": get_verb_phrases(sent),
        "nounphrase": get_noun_phrases(sent)
    }
    parsed["semparse"] = {}
    parsed["triples"] = get_svo_triples(sent)

    constituency = get_constituency(sent)
    parsed["constituency"] = str(constituency)

    return parsed


def get_constituency(sent):
    return sent._.parse_string


def get_verb_phrases(sent):
    chunks = []
    pattern = r'<VERB>?<ADV>*<VERB>+'

    pattern = [{'POS': 'VERB', 'OP': '?'},
               {'POS': 'ADV', 'OP': '*'},
               {'POS': 'VERB', 'OP': '+'}]

    lists = textacy.extract.token_matches(sent, pattern)
    for chunk in lists:
        chunks.append(chunk.text)
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


def analyze_passage(passage, context="default"):
    doc = textacy.make_spacy_doc(passage, lang=en)

    logger.info(f"Type (doc): {type(doc)}")

    out = {"passage": passage, "context": context, "sentences": []}

    k = 0
    for sent in doc.sents:

        logger.info(f"Type (sent): {type(doc)}")

        parsed = analyze_sentence(sent, out)

        if not parsed:
            continue

        out["sentences"].append(parsed)
        k = k + 1

    return out


def cleanup_tree(ptree, remove_first_line=True):
    if remove_first_line:
        ptree = '\n'.join(ptree.split('\n')[1:])

    ptree = ptree.replace("\n", " ")
    ptree = re.sub(' {2,}', ' ', ptree)
    return ptree


def extract_sentence_meta(sent: object, out):
    if len(sent.text.strip()) < 1:
        return False

    parsed: dict[str, object] = {
        "sentence": sent.text,
        "wordtypes": get_word_types(sent),
        "ner": get_named_entities(sent),
        "wordnet": get_wordnet_hierarchy(sent),
        "syntaxparse": {
            "verbphrase": get_verb_phrases(sent),
            "nounphrase": get_noun_phrases(sent)
        },
        "semparse": {
            "amr": cleanup_tree(sent._.to_amr()[0]),
        },
        "triples": get_svo_triples(sent),
        "constituency": str(get_constituency(sent)),
        "logic": {
            "fol": {},  # str(text2logic(sent.text, False)),
            "json": str(generate_clauses(cleanup_tree(sent._.to_amr()[0])))
        }
    }

    return parsed


def extract_meta(passage: str, context="default", message=False):
    doc = textacy.make_spacy_doc(passage, lang=en)
    # print("extract_meta():", message)

    meta = {"passage": passage, "context": context, "sentences": []}

    k = 0
    for sent in doc.sents:
        parsed = extract_sentence_meta(sent, meta)

        if not parsed:
            continue

        meta["sentences"].append(parsed)
        k = k + 1

    return meta


def format_constant(txt):
    """
    Constants are lowercase
    """
    ret = txt.lower().strip('"')
    return ret


def format_clause(txt):
    """
    Remove AMR specific clause modifiers, e.g :ARG0 is transformed to ARG1
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


def generate_clauses(amr_string):
    """
    Generate clauses from AMR string
    """
    g = penman.decode(amr_string)

    constant_dict = {}
    for c in g.attributes():
        constant_dict[c[0]] = c[1]

    clauses = []

    # Get base concepts
    for inst in g.instances():
        value = format_variable(inst[0])

        # We do not create clauses for constants
        if inst[0] in constant_dict:
            continue

        arity = max(
            len(g.edges(source=inst[0])),
            len(g.edges(target=inst[0]))
        )

        expr = [inst[2], value]
        if arity > 1:
            for edge in g.edges(source=inst[0]):
                val = format_variable(edge[2])
                if edge[2] in constant_dict:
                    val = format_constant(edge[2])
                expr.append(val)
        clauses.append(expr)

    # Get concept relations
    for rel in g.edges():
        value = format_variable(rel[2])
        constants = g.attributes(source=rel[2])
        if len(constants) > 0:
            value = format_constant(constants[0][2])

        predicate = format_clause(rel[1])

        if predicate in role_dict.keys():
            predicate = role_dict[predicate]

        clause = [
            predicate,
            format_variable(rel[0]),
            value]
        clauses.append(clause)

    # return json.dumps(intersperse(clauses, "&"))
    return json.dumps(clauses)


def passage2logic(passage, debug=False):
    doc = textacy.make_spacy_doc(passage, lang=en)
    graphs = doc._.to_amr()

    meta = extract_meta(passage, "default", "passage_to_logic()")

    i = 0
    for sent in list(doc.sents):
        logic = generate_clauses(graphs[i])
        if debug:
            print("SENT:", sent)
            print("META", meta["sentences"][i])
            print("AMR:", cleanup_tree(graphs[i]))
            print("LOGIC:", logic)
            print("---")
        i = i + 1


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("No input passage provided")
        sys.exit()

    passage = sys.argv[1]
    passage_meta = extract_meta(passage, "default", "__main__")
    print(json.dumps(passage_meta, indent=2))
