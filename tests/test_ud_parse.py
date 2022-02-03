import json
import re
from pprint import pprint

ud = "(S (NP (NNP Tallinn)) (VP (VBZ is) (NP (NP (DT a) (NN capital)) (PP (IN of) (NP (NNP Estonia))))) (. .))"


def ud_to_json(parse):
    p = parse.replace("(", "[")
    p = p.replace(")", "]")
    p = p.replace(") (", "],[")
    p = re.sub(r'([a-zA-Z]+)', r'"\1"', p)
    # p=re.subn("([a-z]*)","*",p, count=1000, flags=0)
    p = p.replace(" ", ",")
    p = p.replace(".,.", "\".\",\".\"")
    p = p.replace(", ,", "\",\",\",\"")
    p = p.replace("[,,,]", "[\",\",\",\"]")

    tree = json.loads(p)
    return tree


def get_list_el(lst, tag):
    """
    get_list_el(tree, "ADVP")
    """
    if not lst: return None
    i = 0
    while i < len(lst):
        el = lst[i]
        if type(el) == list:
            if el[0] == tag:
                return el
        i += 1
    return None


def get_list_word(lst, word):
    match = None
    for idx, el in enumerate(lst):
        if type(el) == list and not match:
            if el[1] == word:
                match = el
            else:
                if get_list_word(el, word):
                    match = get_list_word(el, word)
    return match



def get_list_elword(lst, tag):
    """
    get_list_elword(vp, "VBD")
    """
    tmp = get_list_el(lst, tag)
    if not tmp: return None
    return tmp[1]


if __name__ == "__main__":

    ud_lst = ud_to_json(ud)

    print(ud)
    pprint(ud_lst, indent=2)
    print("---")
    print(get_list_elword(ud_lst, "VP"))
    print("---")
    print(get_list_word(ud_lst, "Estonia"))