import sys
import warnings

import udutil
import config


def get_root(amr_graph):
    """
    Extract root lemma and type for AMR graph
    :param amr_graph:
    :return:
    """
    root_instance = amr_graph[0][1].split("-", 1)[0]
    # print(amr_graph[0][1], "->", root_instance)
    root_word = udutil.get_word(config.snt_ud, root_instance)
    if root_word:
        return {"upos": root_word["upos"], "lemma": root_word["lemma"]}
    return None


def check_edge(edge, parent):
    return
    print("Parent:", parent)
    print("Edge", edge)


def parse_init_root(json_list, edge):
    root = get_root(json_list)
    if root:
        lemma = root["lemma"]
        upos = root["upos"]
        rtype = "instance"
        if "NOUN" == upos:
            rtype = "isa"
        return [rtype, lemma, edge[0]]
    else:
        return [edge[1], edge[0]]


def extract_name_variable(edge):
    names = [it[1] for it in edge[2:]]
    return ["name", "_".join(names)]


count = 0
relations = []


def extract_relations(lst, parent=None, debug=False):
    global relations
    for edge in lst:
        if isinstance(edge, list) and isinstance(edge[0], str) and isinstance(edge[1], str):
            if parent:
                if edge[0] == ":polarity":
                    edge.reverse()
                if debug: print(f"var: {edge[1]} := {edge[0]} (parent={parent})")
                relations.append([edge[1], edge[0], parent])
            else:
                if debug: print(f"var: {edge[1]} := {edge[0]}")
                if not parent:
                    relations = []
                    parent = edge[0]
                    relations.append([edge[1], edge[0], None])

        if isinstance(edge, list) and isinstance(edge[0], str) and isinstance(edge[1], list):
            # print(f"edge: {edge[0]} ({len(edge[1:])}): {edge[1:]}")
            if debug: print(f"rel: edge := '{edge[0]}' parent := '{parent}'")
            relations.append(["relation", edge[0], parent])
            extract_relations(edge[1:], edge[0], debug)
    return relations




"""
def parse_logic_list(lst, parent=None):
    for edge in lst:
        if isinstance(edge, list):

            # [':instrument', ['k', 'knife']]
            if len(edge) == 2 and isinstance(edge[1], list) or len(edge) > 2:
                print("Further:", edge)
                parse_logic_list(edge, parent)

            parent = edge[0]

        print("len:", len(edge), "parent: ", parent, edge)
"""


def parse_logic_list_(json_list, depth=0, parse=[]):
    global count

    print("Parse:", count, json_list)
    count += 1

    if isinstance(json_list, list):
        for edge in json_list:
            print(f"{depth * ''}Depth={depth}, edge={edge}")
            if not parse:
                parse.append(parse_init_root(json_list, edge))
                continue
            if ":name" == edge[0]:
                parse.append(extract_name_variable(edge))
                del edge
                continue
            if ":polarity" == edge[0]:
                warnings.warn("Parsing polarity")
            if isinstance(edge, list):
                parse_logic_list(edge, depth + 1, parse)

    print(parse)
    print("Finalcount", count)
    return parse

    # print(parse)
    # sys.exit(-1)
