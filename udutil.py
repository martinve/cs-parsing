import sys

"""
Utilities for extracting informatin from Universal Dependencies
"""


def get_named_entities(snt_ud):
    """
    Get a list of named entities via token BIOES representation
    :param snt_ud: UD graph
    :return: dictionary of named entities and its prefix
    """

    entities_lst = []
    name_lst = []

    for tok in snt_ud:
        if tok["ner"] == "O":
            continue

        prefix = tok["ner"][0]

        if prefix == "B":
            name_lst = [tok["text"]]
        elif prefix == "I-":
            name_lst.append(tok["text"])
        elif prefix in ["E", "S"]:
            name_lst.append(tok["text"])
            entities_lst.append({
                "text": "_".join(name_lst),
                "prefix": tok["ner"][2:]}
            )
            name_lst = []

    return entities_lst
