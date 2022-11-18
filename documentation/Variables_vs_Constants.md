# Variables vs Constants

Given a set of clauses we simplify this - and determine whether we can define the rules as constants or a variable.



John is a man. (Fact)

`isa(john, man)`







Elephants are big. (Concept) 

`isa(X, elephant) => property(big, X)`




Elephants 



+----------+--------------+--------+------+----------+-------+-----------+--------+--------+
| Deprel   | Feats        |   Head |   ID | Lemma    | NER   | Text      | upos   | xpos   |
+==========+==============+========+======+==========+=======+===========+========+========+
| nsubj    | Number=Plur  |      4 |    1 | elephant | O     | Elephants | NOUN   | NNS    |
+----------+--------------+--------+------+----------+-------+-----------+--------+--------+
| cop      | Mood=Ind     |      4 |    2 | be       | O     | are       | AUX    | VBP    |
|          | Tense=Pres   |        |      |          |       |           |        |        |
|          | VerbForm=Fin |        |      |          |       |           |        |        |
+----------+--------------+--------+------+----------+-------+-----------+--------+--------+
| advmod   |              |      4 |    3 | not      | O     | not       | PART   | RB     |
+----------+--------------+--------+------+----------+-------+-----------+--------+--------+
| root     | Degree=Pos   |      0 |    4 | small    | O     | small     | ADJ    | JJ     |
+----------+--------------+--------+------+----------+-------+-----------+--------+--------+
| punct    |              |      4 |    5 | .        | O     | .         | PUNCT  | .      |
+----------+--------------+--------+------+----------+-------+-----------+--------+--------+ 

