import nltk
from nltk.corpus import propbank

# see: https://sites.pitt.edu/~naraehan/ling1330/lecture23_PropBank_in_NLTK.html

# nltk.download("propbank")
# nltk.download("treebank")

# color-01

rs = propbank.roleset('abstain.01')

for role in rs.findall('roles/role'):
    print(role.attrib['n'], role.attrib['descr'])