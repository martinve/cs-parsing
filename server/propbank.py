import sys
from nltk.corpus import propbank


# see: https://sites.pitt.edu/~naraehan/ling1330/lecture23_PropBank_in_NLTK.html

# nltk.download("propbank")
# nltk.download("treebank")

# color-01

def describe(roleset_id):
    try:
        rs = propbank.roleset(roleset_id)
        for role in rs.findall('roles/role'):
            print(f"ARG{role.attrib['n']}: {role.attrib['descr']}")
    except ValueError:
        print(f"No PropBank role found for {roleset_id}")
    print("---")


def sample():
    for item in ["abstain.01", "like.01", "stab.01", "color.01"]:
        describe(item)


if __name__ == "__main__":

    inp = False

    if len(sys.argv) > 1:
        inp = sys.argv[1]

    if inp:
        describe(inp)
