# Classificattion sentence

The sentence can be classified as:

* Abstract - describing conceptual knowledge. 
* Fact - describing concrete facts.
* Situational - describing activities and situations.

Rules

* If the sentence contains named entity then NOT_ABSTRACT
* If the sentence contains a definite article *the*, then NOT_ABSTRACT
* For verbs:
  * If sentence contains is/be/have then NOT_SITUATIONAL
  * For other verbs: SITUATIONAL
* If it is not clear if it is abstract or "Elephants eat plants."
  * All elephants eat plants - markeerimine
  * Otherwise context.


Corpus for each types of sentences

* Abstract: Quasimodo
* Fact: DBPedia
* Situational: Winograd schema challenge.







If POS is in snt, then not ABSTRACT
If "The" in snt, then not ABSTRACT 

if FACT or SIT:
	
Is/be/are/having etc. - ei muuda SIT
if other verbs - SIT	


"Elephants eat plants." - abstract until other references (this/it/that) are in passage.

Situational:
 - Add points for heuristics. (a - some pts towards SIT, the - adds much MORE, singular word - )


TODO: Calculate the confidence for each classfification



SIT, FACT, ABSTRACT




The Cat is red. - S
Cat is an animal. - A weakly abstact (needs context)
All cats are animals. - A (tuleb sellest et pole mitteabstraktseid komponente) - et muuta F tuleks leida värki mis muudab selle mitteaA.
Some cats are animals. - A



Inglise keeles:
Kõik konkreetsed asjad #the


catch-01 


? TODO: F


Corpus:
1. Situational - Winograd
2. Abstract - Quasimodo
3. Fact - ?https://github.com/dbpedia/fact-extractor

Inglise keel: https://core.ac.uk/download/pdf/211329362.pdf

@see also: Semantic Ambiguity and Perceived Ambiguity. https://arxiv.org/pdf/cmp-lg/9505034.pdf