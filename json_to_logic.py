import json
import pprint
import sys

from amr_to_json import amr_to_json
from logger import logger
from types_util import is_string, is_op, is_list, is_atom

logic_lst = []
debug = True

role_dict = {
    ":arg0": "agent",
    ":arg1": "patient",
    ":arg2": "instrument",
    ":arg3": "startingPoint",
    ":arg4": "endingPoint",
    ":arg5": "modifier",
    ":domain": "isa"
}


def list_depth(lst):
    if isinstance(lst, list):
        return 1 + max(list_depth(item) for item in lst) if lst else 0
    else:
        return 0


def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result


def is_variable_assignment(cl):
    return len(cl) == 2 and is_string(cl[0]) and is_string(cl[1])


def add_clause(stmt, debug_msg):
    logic_lst.append(stmt)
    if debug and debug_msg:
        logger.info(f"ADD ({debug_msg}): {stmt}")


def add_question(json_logic, question):
    if question:
        try:
            question = json.loads(question)
            json_logic.append({"@question": question})
        except:
            logger.error("Error: Invalid question")
            logger.error(question)
            sys.exit(-1)
    return json_logic


def add_question_clauses(json_logic, question):
    ques = pprint.pformat(question, indent=2, compact=False)

    if not is_list(question):
        logger.error("Provided questions not a list.")
        logger.error(f"Ques: \n{ques}")
        sys.exit(-1)

    for idx, cl in enumerate(question):
        if "amr-unknown" == cl[1]:
            question.pop(idx)
            # pass

    logger.debug(f"Provided question: \n{ques}")
    json_logic.append({"@question": question})
    return json_logic


def extract_name(cl):
    names = []
    for e in cl:
        if not is_list(e):
            continue
        if e[0][0:3] == ":op":
            names.append(e[1].lower())
    return "_".join(names)


def replace_role(arg):
    return arg

    # TODO: uncomment, check exception

    rel = arg.lower()
    return rel

    if rel in role_dict.keys():
        rel = role_dict[arg]
    return argcl


def parse_edge(edge, parent, debug=False):
    if debug:
        logger.debug(f"IN_0 ({parent}): {edge}")

    value = edge[0:2]
    modifier = edge[2:]

    if debug:
        logger.info(f"IN_1: val({list_depth(value)})={value}, modifier({list_depth(modifier)})={modifier}")

    # print(f"p={parent}, len={len(val)}, elen={len(edge)}, val={val}")
    # logger.debug(f"val={len(val)}, edge={len(edge)}")

    # variable assignment is in form [instance, var] e.g. [flag, f]
    if is_variable_assignment(edge):
        logger.debug(f"ISA: {edge}")
        if is_op(edge[0]):
            stmt = [parent, edge[1]]
            add_clause(stmt, "add_op")
        else:
            raise ValueError("Edge must be list", edge, parent)

    # Operator merging
    all_ops = True
    for idx, it in enumerate(edge):
        if not is_op(it[0]):
            all_ops = False
    if all_ops:
        ops = []
        for it in edge:
            ops.append(it[1])

        stmt = [parent, ops]
        add_clause(stmt, "ops")
        return

        # TODO: Merge the operators

    # Name handling
    if ':name' == value[0] and 'name' == value[1][1]:

        # stmt = [val[1][1], val[1][0], parent]
        # add_clause(stmt, "name_val")

        name = extract_name(modifier)
        stmt = ["name", name, parent]
        add_clause(stmt, "extract_name")

        if debug:
            logger.warning(f"Name: {value}, mod={modifier}")
            logger.warning("Return after name val parsing.")
        return
    else:
        rel = replace_role(value[0])
        stmt = [rel, value[1][1], value[1][0]]
        add_clause(stmt, "edge_val")

    parent = edge[1][0]

    if modifier:

        if len(modifier) == 1 and is_list(modifier[0]):
            modifier = modifier[0]

        if value != modifier:
            if not is_atom(modifier):
                parse_edge(modifier, parent)
            else:
                if debug:
                    logger.warning(f"Mofifier: {modifier}, edge={value}, parent={parent}")


def json_list_to_logic(json_list, debug):
    parent_var = None
    for cl in json_list:
        if is_variable_assignment(cl):
            if not parent_var:
                stmt = ["instance", cl[1], cl[0]]
                add_clause(stmt, "assign_var")
                parent_var = stmt
        else:
            parse_edge(cl, parent_var, debug)


def svo_filter(clause_lst, s=None, v=None, o=None):
    ret = []
    for cl in clause_lst:
        if s and cl[0] == s:
            ret.append(cl)
        if v and cl[1] == v:
            ret.append(cl)
        if o and cl[2] == o:
            ret.append(cl)
    return ret


def simplify_clauses(clause_lst):
    logger.info("Simplifying clauses.")
    return clause_lst

    simpl_lst = []

    for idx, cl in enumerate(clause_lst):
        simpl_lst.append(cl)
        if ":poss" == cl[0]:
            find = svo_filter(clause_lst, v=cl[2])
            if find:
                find = find[0]
                if find[0] == "name":
                    clause_lst[idx] = [cl[1], find[2]]
                    clause_lst.remove(find)
            logger.info(f"Find: {find}, search={cl[2]}, res={find}")

    return simpl_lst


def amr_to_logic(amr_str, constituency, debug=False):
    global logic_lst
    logic_lst = []

    json_list = amr_to_json(amr_str, debug=debug)

    if debug:
        pprint.pprint(json_list, indent=2)

    json_list_to_logic(json_list, debug)

    json_logic = logic_lst

    outp = str(json_logic)
    outp = outp.lower()
    outp = outp.replace("'", "\"")
    outp = json.loads(outp)

    if debug:
        print("--- LOGIC (", len(json_logic), ")---")
        pprint.pprint(json_logic)
        print("--- CLAUSES ---")
        pprint.pprint(outp, indent=2)

    # outp = json.loads(outp)
    return outp
