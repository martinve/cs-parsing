from nltk.corpus import wordnet as wn
import argparse


yago_prefix = "10"


def print_syn(syn, prefix = ' '):
    if defs:
        print(prefix, syn.name(), ':', syn.definition())
    elif ids:
        print("wordnet", get_name(syn), get_id(syn), sep="_")
    else:
        print(prefix, syn.name())



def get_parents(syn, arr = []):
    parents = syn.hypernyms()

    if len(parents) > 0:
        parent = parents[0]
        arr.append(parent)
        get_parents(parent, arr)
    else:
        arr.reverse()
        for syn in arr:
            print_syn(syn) 



def get_children(syn):
    synes = not isinstance(syn, (list, tuple)) and [syn] or syn
    depth = [1]

    def wrapped(syn):
        index = '.'.join([str(i) for i in depth])
        
        if len(depth) > 1:
            prefix = " " + (len(depth) - 1) * "  "
            print_syn(syn, prefix)
        
        depth.append(1)

        for child in syn.hyponyms():
            wrapped(child)
            depth[-1] += 1
        depth.pop()

    for syn in synes:
        wrapped(syn)
        depth[0] += 1


def get_name(syn):
    return syn.lemmas()[0].name()

def get_id(syn):
    return yago_prefix +  str(syn.offset())


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Generate facts based on postgresql database")
    parser.add_argument("-s", "--synset", help="Synset, e.g. 'dog.n.01'", required=True)
    parser.add_argument("-d", "--definitions", help="Display definitions", action="store_true")
    parser.add_argument("-i", "--ids", help="Display synset IDs", action="store_true")
    parser.add_argument("-c", "--children", help="Show children", action="store_true")
    args = parser.parse_args()

    defs = args.definitions
    children = args.children
    ids = args.ids


    try:
        syn = wn.synset(args.synset)
    except ValueError:
        print("Did not find matching synset for", args.synset)
        sys.exit()

    print()
    get_parents(syn)


    if children == True:
        if defs:
            print("* ", syn.name(), ':', syn.definition())
        elif ids:
            print("* wordnet", get_name(syn), get_id(syn), sep="_")
        else:
            print("*", syn.name())
        get_children(syn)