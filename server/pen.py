import sys
import pprint
import penman
from penman import Graph, Tree


def replace_role(rel, ignore=True):
    if ignore:
        return rel

    rel_replace_dict = {
        ":domain": "isa",
        ":name": "hasName",
        ":location": "locatedAt",
        ":ARG0": "agent",
        ":ARG1": "patient"
    }
    if rel in rel_replace_dict.keys():
        rel = rel_replace_dict[rel]
    return rel


def debug(lst):
    for src, role, target in lst:
        if role in replace_dict.keys():
            role = replace_dict[role]
        print(src, role, target)
    print(20 * "-", "\n")


def assign_value(o, attrs):
    if o in attrs.keys():
        o = attrs[o]
    return o


def get_root(g):
    for s, v, o in g.instances():
        if s == g.top:
            return [s, v, o]


def simplify_logic(logic):
    assert isinstance(logic, list)

    for clause in logic:
        print("s", clause)

    print("\n")
    return logic


if __name__ == "__main__":
    amr3 = """
    (m / man
      :domain (p / person
            :name (n / name
                  :op1 "Martin"
                  :op2 "Luther")))
    """

    amr4 = """
# ::snt Brutus stabs Caesar with a knife.
(s / stab-01
      :ARG0 (p / person
            :name (n / name
                  :op1 "Brutus"))
      :ARG1 (p2 / person
            :name (n2 / name
                  :op1 "Caesar"))
      :instrument (k / knife))
                        """

    amr1 = """
    (j / join-01 :ARG0 (p / person :name (n / name :op1 "Pierre" :op2 "Vinken") :age (t / temporal-quantity :quant 61 :unit (y / year))) :ARG1 (b / board) :ARG2 (d / director :mod (e / executive :polarity -)) :time (d2 / date-entity :day 29 :month 11))"
    """

    amr2 = """
   # ::snt Nintendo is a company located in Japan.
    (c / company
          :domain c
          :name (n / name
                :op1 "Nintendo")
          :location (c2 / country
                :name (n2 / name
                      :op1 "Japan"))) 
    """

    amr5 = """
    # ::snt Percy is a cat.
    (c / cat
          :domain (p / person
                :name (n / name
                      :op1 "Percy")))
     """

    amr6 = """
    # ::snt Elephants are not small.
    (s / small
          :polarity -
          :domain (e / elephant))
    """

    amr7 = """
    # ::snt The colors of Lithuanian flag are yellow, green and red.
    (c / color-01
          :ARG1 (f / flag
                :mod (c2 / country
                      :name (n / name
                            :op1 "Lithuania")))
          :ARG2 (a / and
                :op1 (y / yellow)
                :op2 (g / green)
                :op3 (r / red)))
    """

    amr8 = """
         (l / live-01
           :ARG0 (p / person :wiki "Steven_Spielberg"
                 :name (n / name :op1 "Steven" :op2 "Spielberg"))
           :location (c / city :wiki "Los_Angeles"
                 :name (n2 / name :op1 "Los" :op2 "Angeles")))
    """

    amr9 = """
         (b / boy
           :quant (b2 / between :op1 4000 :op2 5000))
    """

    amr = amr7

    g: Graph = penman.decode(amr)

# print("[Variables]")
# print(g.variables())

print("[Attributes]")
attrs = {}
polarity = []
for s, v, o in g.attributes():
    print(s, v, o)
    if v == ":polarity":
        polarity.append([s, o])

    if s not in attrs.keys():
        attrs[s] = []

    o = o.strip('\"')
    attrs[s].append(o)

for a in attrs.keys():
    if isinstance(attrs[a], list):
        attrs[a] = "_".join(attrs[a])

print(attrs)
print(20 * "=", "\n")

print("[Relations]")
relations = []
for s, v, o in g.edges():
    if s == o:
        continue
    #
    # print(s, v, o)
    rel = [replace_role(v), s, assign_value(o, attrs)]
    relations.append(rel)
print(relations)
print(20 * "-", "\n")

print("[Concepts]", len(g.instances()))
concepts = []
connectives = {}
for s, v, o in g.instances():
    if o in ["name"]:
        continue
    if polarity:
        for p in polarity:
            if p[0] == s:
                o = "-" + o
    if o in ["and", "or"]:
        connectives[s] = o
        continue
    concepts.append([o, s])
print(concepts)
print("Connectives:", connectives)
print(20 * "-", "\n")


print("[Triples]:", len(g.triples))
triples = []
for s, v, o in g.triples:
    triples.append([s, v, o])
print(triples)

"""
print("[Simplified]:")
for s, v, o in triples:
    if s == o:
        continue
    if v == ":instance":
        continue
    print(s, v, o)
"""

print("Logic:")
logic = concepts + relations

logic = simplify_logic(logic)

pprint.pprint(logic)

root = get_root(g)

# Graph instances -> concepts


"""
('[["stab-01", "S", "P", "P2", "K"], ["person", "P"], ["person", "P2"], '
'["knife", "K"], ["agent", "S", "P"], ["name", "P", "brutus"], ["patient", '
'"S", "P2"], ["name", "P2", "caesar"], ["instrument", "S", "K"]]')
"""
