import config
from debugger import print_sentence_tree
from nlpproperlogic import get_children


def prepare_question_sentence(sentence):
    root = get_root(sentence)

    subjword = get_word_by_keyval(get_children(sentence, root), "deprel", "nsubj")

    end_punct = sentence[-1]
    if (end_punct and end_punct["lemma"] == "?" and
            (root['upos'] == "PRON" and root['lemma'] in ["who", "what"])):
        debug_print("====== original question sentence ==========\n")
        print_sentence_tree(sentence)
        text = make_text_from_doc(sentence)
        newtext = replace_text_word(text, root['text'], dummy_name)
        debug_print("replacement text for question:", newtext)
        data = server_parse(newtext)
        sentence = data["doc"][0]
        # debug_print("sentence with a dummy name for question",sentence)
    elif (end_punct and end_punct["lemma"] == "?" and
          (subjword and subjword['upos'] == "PRON" and subjword['lemma'] in ["who", "what"])):
        debug_print("====== original question sentence ==========\n")
        print_sentence_tree(sentence)
        text = make_text_from_doc(sentence)
        newtext = replace_text_word(text, subjword['text'], dummy_name)
        debug_print("replacement text for question:", newtext)
        data = server_parse(newtext)
        sentence = data["doc"][0]
    return sentence




# ====== debug printing and error handling ==========

def debug_print(label, data="placeholder"):
    if not parser_config.debug_print_flag: return
    print()
    print(label, end='')
    if data == "placeholder":
        print()
        return
    if type(data) == list:
        print(":")
        for el in data:
            print(" ", el)
    elif type(data) == dict:
        print(":")
        for key in data:
            print(" ", key, ":", data[key])
    else:
        print(" :", data)


def debug_pprint(label, data="placeholder"):
    if not parser_config.debug_print_flag: return
    print()
    print(label, end='')
    if data == "placeholder":
        print()
        return
    if type(data) == list:
        print(":")
        pprint.pprint(data)
    elif type(data) == dict:
        print(":")
        pprint.pprint(data)
    else:
        print(" :", data)


# ===== composing a text from the parse tree ===

def make_text_from_doc(doc):
    if not doc: return ""
    lastpos = 0
    firstpos = 100000000
    for word in doc:
        if ("end_char" in word) and word["end_char"] > lastpos:
            lastpos = word["end_char"]
        if ("start_char" in word) and word["start_char"] < firstpos:
            firstpos = word["start_char"]
    s = ' ' * ((lastpos - firstpos) + 1)
    for word in doc:
        s = s[0:(word["start_char"] - firstpos)] + word["text"] + s[(word["end_char"] - firstpos):]
    return s


def replace_text_word(text,what,to):
  sp=text.split(" ")
  newsp=[]
  for el in sp:
    if el==what:
      newsp.append(to)
    elif el.lower()==what:
      newsp.append(to)
    else:
      newsp.append(el)
  return " ".join(newsp)
