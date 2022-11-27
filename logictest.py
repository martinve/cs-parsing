"""
Test logical conversion
"""
import penman
import difflib

from amrutil import replace_role, assign_value

amr = """
# ::snt Mike is a mouse.
(m / mouse
      :domain (p / person
            :name (n / name
                  :op1 "Mike")))
  """

amr1 = """
# ::snt Donald Trump and Barack Obama were  presidents of United States of America.
(h / have-org-role-91
      :ARG0 (a / and
            :op1 (p / person
                  :name (n / name
                        :op1 "Donald"
                        :op2 "Trump"))
            :op2 (p2 / person
                  :name (n2 / name
                        :op1 "Barack"
                        :op2 "Obama")))
      :ARG1 (c / country
            :name (n3 / name
                  :op1 "United"
                  :op2 "States"
                  :op3 "of"
                  :op4 "America"))
      :ARG2 (p3 / president))
"""

amr2 = """
# ::snt Barack Obama was a president of United States of America.
(h / have-org-role-91
      :ARG0 (p / person
            :name (n / name
                  :op1 "Barack"
                  :op2 "Obama"))
      :ARG1 (c / country
            :name (n2 / name
                  :op1 "United"
                  :op2 "States"
                  :op3 "of"
                  :op4 "America"))
      :ARG2 (p2 / president))
"""


class Parser:
    def __init__(self, amr_str):
        self.amr = amr_str
        self.logic = None
        self.concepts = None
        self.relations = None
        self.attributes = None

    def parse(self):
        g = penman.decode(self.amr)

        attrs = {}
        polarity = []
        for s, v, o in g.attributes():
            if v == ":polarity":
                polarity.append([s, o])
                continue

            if s not in attrs.keys():
                attrs[s] = []

            o = o.strip('\"')
            attrs[s].append(o)

        for a in attrs.keys():
            if isinstance(attrs[a], list):
                attrs[a] = "_".join(attrs[a])


        concepts = []
        for s, v, o in g.instances():
            if o not in ["name"]:
                for p in polarity:
                    if p[0] == s:
                        o = "-" + o
                concepts.append([o, s.upper()])

        rels = []
        for s, v, o in g.edges():
            if s == o:
                continue
            # rel = [replace_role(v), s, assign_value(o, attrs)]
            rel = [v, s, assign_value(o, attrs)]
            rels.append(rel)

        self.attributes = attrs
        self.relations = rels
        self.concepts = concepts

        self.logic = concepts + rels


def rewrite_graph(amr_str):
    from penman.codec import PENMANCodec
    from penman.models.amr import model
    from penman.transform import canonicalize_roles
    codec = PENMANCodec()
    t = codec.parse(amr_str)


    t = canonicalize_roles(t, model)
    return codec.format(t)


def main(amr_str):
    parser = Parser(amr_str)
    parser.parse()

    print("Concepts", parser.concepts)
    print("Relations", parser.relations)
    print("Attributes", parser.attributes)
    print("---")
    print("Logic", parser.logic)


if __name__ == "__main__":
    a = amr2
    a_ = rewrite_graph(a)

    if a != a_:
        for i, s in enumerate(difflib.ndiff(a, a_)):
            if s[0] == ' ':
                continue
            elif s[0] == '-':
                print(u'Delete "{}" from position {}'.format(s[-1], i))
            elif s[0] == '+':
                print(u'Add "{}" to position {}'.format(s[-1], i))


                # main(amr2)
