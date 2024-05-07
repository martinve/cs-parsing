import penman
import pprint
import difflib as dl

from amrutil import replace_role, assign_value


"""
Test logical conversion
"""

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

amr3 = """
# ::snt The boy from college sang
(b / boy
   :ARG0-of (s / sing-01)
   :source (c / college))
"""


class Parser:
    def __init__(self, amr_str):
        self.amr = amr_str
        self.logic = None
        self.concepts = None
        self.relations = None
        self.attributes = None
        self.triples = None

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
        self.triples = g.triples

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

    c = parser.concepts
    r = parser.relations
    a = parser.attributes
    t = parser.triples

    print(amr_str)
    print("---")

    for rel in r:
        print("Rel: ", rel)

    for c_ in c:
        print("C:", c_)

    for arg in a:
        print("Arg:", arg)

    print("Triples: ", len(t))
    for triple in t:
        print("Triple:", triple)

    print("Concepts:", c)
    print("Relations:", r)
    print("Attributes:", a)
    print("Triples:", t)
    print("---")
    print("Logic:", parser.logic)


def visualize(nodes, relations):
    import networkx as nx
    import matplotlib.pylab as plt

    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(relations)

    # extract the attribute 'action' from edges
    edge_attribute = nx.get_edge_attributes(G, 'action')
    edges, weights = zip(*edge_attribute.items())
    # resize figure
    plt.rcParams["figure.figsize"] = [5, 2]
    plt.rcParams["figure.autolayout"] = True
    # set figure layout
    pos = nx.circular_layout(G)
    # draw graph
    nx.draw(G, pos, node_color='b', width=2, with_labels=True)
    # draw edge attributes
    nx.draw_networkx_edge_labels(G, pos,edge_attribute, label_pos=0.75 )
    plt.show()


def parse(amr_str):
    parser = Parser(amr_str)
    parser.parse()

    nodes = []
    relations = []
    # iterate over the triples
    for subject, verb, object in parser.triples:
        # extract the Subject and Object from triple
        node_subject = subject # "_".join(map(str, subject))
        node_object  = object # "_".join(map(str, object))
        nodes.append(node_subject)
        nodes.append(node_object)
        # extract the relation between S and O
        # add the attribute 'action' to the relation
        relation = verb # "_".join(map(str, verb))
        relations.append((node_subject,node_object,{'action':relation}))
    # remove duplicate nodes
    nodes = list(set(nodes))
    print(nodes)
    # ['to_extract_SVO', 'I']
    print(relations)
    # [('I', 'to_extract_SVO', {'action': 'am_going'})]

    visualize(nodes, relations)


def rewrite(amr_graph, debug=False):
    amr_ = rewrite_graph(amr_graph)

    if amr_ == amr:
        return amr

    if debug:    

        print("AMR", amr_graph)
        print("AMR_", amr_)

        s1 = [x.strip() for x in amr_graph.split("\n")]
        s2 = [x.strip() for x in amr_.split("\n")]

        print(s1)
        print(s2)

        diffs = dl.context_diff(s1, s2)
        diffs = dl.unified_diff(s1, s2)
        # diffs = dl.ndiff(s1, s2)

        for diff in diffs:
            print(diff)

    return amr_

    """
    for i, s in enumerate(diff):
        if s[0] == ' ':
            continue
        elif s[0] == '-':
            print(u'Delete "{}" from position {}'.format(s[-1], i))
        elif s[0] == '+':
            print(u'Add "{}" to position {}'.format(s[-1], i))
    """



if __name__ == "__main__":

    g = amr1.strip()
    g_ = rewrite(g)
    #main(g_)
    parse(g)
    print("Done.")
