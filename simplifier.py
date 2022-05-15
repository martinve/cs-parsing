from logger import logger
from tests.sentence_heuristic_classifier import snt_type_label


def simplify(clauses, snt_type):
    # logger.info(f"Simpl: len(initial): {len(clauses)}, snt_type={snt_type_label(snt_type)}")

    # TODO: Implemenet clause simplifier

    var_dict = {}
    for cl in clauses:
        # logger.info(f"Clause: {cl}")
        if len(cl) == 2 and isinstance(cl[0], str) and isinstance(cl[1], str):
            var_dict[cl[0]] = cl[1]

    # logger.info(f"Variables: {var_dict}")