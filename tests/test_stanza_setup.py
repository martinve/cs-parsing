import stanza
import spacy_stanza
from tabulate import tabulate

# Download the stanza model if necessary
# stanza.download("en")

# Initialize the pipeline
nlp = spacy_stanza.load_pipeline("en")

doc = nlp("Barack Obama was born in Hawaii. He was elected president in 2008.")

table = [["Text", "Lemma", "Pos", "Dep", "Ent. Type"]]
for token in doc:
    table.append([token.text, token.lemma_, token.pos_, token.dep_, token.ent_type_])


print( tabulate(table, headers=("firstrow")))

print("--")

print(doc.ents)