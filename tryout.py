import amrutil


def extract_relations(lst, parent=None):
    for edge in lst:
        if isinstance(edge, list) and isinstance(edge[0], str) and isinstance(edge[1], str):
            if parent:
                if edge[0] == ":polarity":
                    edge.reverse()
                print(f"var: {edge[1]} := {edge[0]} (parent={parent})")
            else:
                print(f"var: {edge[1]} := {edge[0]}")
                if not parent:
                    parent = edge[0]

        if isinstance(edge, list) and isinstance(edge[0], str) and isinstance(edge[1], list):
            # print(f"edge: {edge[0]} ({len(edge[1:])}): {edge[1:]}")
            print(f"rel: edge := '{edge[0]}' parent := '{parent}'")
            extract_relations(edge[1:], edge[0])


if __name__ == "__main__":

    # Elephants are not small
    json_list_0 = [['s', 'small'], [':polarity', '-'], [':domain', ['e', 'elephant']]]

    # Brutus stabs Caesar with a knife
    json_list_1 = [['s', 'stab-01'],
                    [':ARG0', ['p', 'person'], [':name', ['n', 'name'], [':op1', 'Brutus']]],
                    [':ARG1', ['p2', 'person'], [':name', ['n2', 'name'], [':op1', 'Caesar']]],
                    [':instrument', ['k', 'knife']]]

    # Donald Trump and Barack Obama were presidents of United States of America.
    json_list_2 = [['h', 'have-org-role-91'],
                    [':ARG0', ['a', 'and'],
                     [':op1', ['p', 'person'],
                      [':name', ['n', 'name'], [':op1', 'Donald'], [':op2', 'Trump']]],
                     [':op2', ['p2', 'person'],
                      [':name', ['n2', 'name'], [':op1', 'Barack'], [':op2', 'Obama']]]],
                    [':ARG1', ['c', 'country'],
                     [':name', ['n3', 'name'], [':op1', 'United'], [':op2', 'States'],
                      [':op3', 'of'], [':op4', 'America']]],
                    [':ARG2', ['p3', 'president']]]

    # Elephants are not small.
    json_list_3 = [['s', 'small'], [':polarity', '-'], [':domain', ['e', 'elephant']]]

    # todo: set sentence UD for config
    extract_relations(json_list_3)
