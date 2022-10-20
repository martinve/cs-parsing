

# Exploring Wordnet taxonomies

To visualize the hierarchical representations in Wordnet a command-line tool was created

**Usage:**

Get the taxonomy tree for a word:

`python3 db_wordnet_tree.py -s n.01.dog`

Get the the taxonomy tree for the word and generate IDs:

`python3 db_wordnet_tree -s n.01.dog <-i> --ids`

Get the taxonomy tree for the word and display descriptions

`python3 db_wordnet_tree -s n.01.dog <-i> --descriptions`

