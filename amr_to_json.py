import json
import re
from logger import logger

failed = []


def add_quotes(s):
    ret = re.sub(r'(:?[a-zA-Z0-9-]+)', r'"\1"', s)
    # TODO: Cleaner solution
    return ret.replace('""', '"')


def amr_to_json(amr_str, debug=False):
    depth = 0
    ret = []
    read_op = False
    edge_op = True
    extra_bracket = 0

    for char in amr_str:

        outp = "".join(ret)

        if char == "(":
            char = "["
            depth = depth + 1
        elif char == ")":
            char = "]"
            if extra_bracket:
                if debug:
                    logger.debug(f"Extra ], d={depth}, e={extra_bracket}")
                char = (1 + extra_bracket) * "]"
                extra_bracket = 0
            depth -= 1
        elif char == "/":
            char = ","
        elif char == ":":
            if debug:
                logger.debug(f": op={int(read_op)}, d={depth}, e={extra_bracket}, {outp}")

            if edge_op:
                ret.append("]")
                extra_bracket -= 1
                edge_op = False

            ret.append(",[")
            extra_bracket += 1
            depth += 1

            read_op = True
            edge_op = True

            # print(f": d={depth}, e={extra_bracket}", outp)
        elif char == " ":
            if read_op:
                char = ","
                read_op = False
            else:
                char = ""

        ret.append(char)

    ret = "".join(ret)
    ret = add_quotes(ret)
    ret = f"[{ret}]"

    return_arr = []
    try:
        return_arr = json.loads(ret)
    except:
        logger.error(f"err: {ret}")
        failed.append(ret)

    if debug:
        logger.info(f"str: {ret}")
        logger.info(f"lst: {return_arr}")

    return return_arr
