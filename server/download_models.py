import stanza, spacy, benepar, nltk

"""
Load the models for initialization. 
Run this first time after installation before running the server.

"""

if __name__ == "__main__":
    nltk.download('omw-1.4')
    stanza.download("en")
    spacy.cli.download("en_core_web_sm")
    benepar.download('benepar_cen3', quiet=True)
