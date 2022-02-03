from amr_to_json import amr_to_json
from json_to_logic import json_list_to_logic, logic_lst, simplify_clauses
from pprint import pprint

if __name__ == "__main__":

    amr = '(c / color-01 :ARG1 (f / flag :poss (c2 / country :name (n / name :op1 \"Lithuania\"))) :ARG2 (a / and :op1 (y / yellow) :op2 (g / green) :op3 (r / red)))'

    amr = '(a / and :op1 (c / color :mod (r / red)) :op2 (c2 / color :mod (w / white)) :domain (f / flag :poss (c3 / country :name (n / name :op1 \"Lettonia\"))))'

    amr = '(j / join-01 :ARG0 (p / person :name (n / name :op1 "Pierre" :op2 "Vinken") :age (t / temporal-quantity :quant 61 :unit (y / year))) :ARG1 (b / board) :ARG2 (d / director :mod (e / executive :polarity -)) :time (d2 / date-entity :day 29 :month 11))'

    clauses = amr_to_json(amr)
    json_list_to_logic(clauses, debug=True)

    logic = logic_lst

    simplified = simplify_clauses(logic)

    print("--- AMR ---")
    pprint(amr)

    print("--- CLAUSES ---")
    pprint(clauses, indent=2)

    if clauses != simplified:
        print("--- SIMPLIFIED ---")
        pprint(simplified, indent=2)

    print("--- LOGIC ---")
    pprint(logic, indent=2)

