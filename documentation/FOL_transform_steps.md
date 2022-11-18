# Parallel Parsers

Parallel parsing environment

## Pre-Requisites

Docker needs to be installed on host machine.

## Installation 

`git clone` and `cd parallel_parsing`

## Usage:
* `build.sh` - build the environment
* `parse.sh infile.json` - run the parsers on input file. The path to input file is relative to current working directory. 

## Example:
`./build.sh && ./parse.sh data/vinken.json`




## Input and Output


The data files reside in `data` directory that is mounted to docker instance volume.


#### Sample Input

```
{
    "question": "John bought some apples. John ate one. Then he bought an Apple laptop",
    "context": "news"
}
```

#### Sample Output

```
{
  "question": "John bought some apples.",
  "context": "news",
  "sentences": [
    {
      "sentence": "John bought some apples.",
      "wordtypes": {
        "PROPN": ["John"],
        "VERB": ["bought"],
        "DET": ["some"],
        "NOUN": ["apples"],
        "PUNCT": ["."]       ]
      },
      "ner": {
        "PERSON": ["John"]
      },
      "wordnet": [
        {
          "word": "bought",
          "syn": "buy.v.01",
          "parents": [
            "get.v.01"
          ]
        },
        {
          "word": "apples",
          "syn": "apple.n.01",
          "parents": [
            "edible_fruit.n.01",
            "fruit.n.01",
            "reproductive_structure.n.01",
            "plant_organ.n.01",
            "plant_part.n.01",
            "natural_object.n.01",
            "whole.n.02",
            "object.n.01",
            "physical_entity.n.01",
            "entity.n.01"
          ]
        }
      ],
      "syntaxparse": {
        "verbphrase": {},
        "nounphrase": [
          "John",
          "some apples"
        ]
      },
      "semparse": {}
    }
  ]
}
```

## Constructing the logical form

Construction of logical form consists of the following steps:

1. Find predicates, specify their arguments (number, type)

   1.1 Concepts and events - predicate/1

   1.2 Roles - predicate/2

2. Construct corresponding atoms

3. Divide atoms on same level into groups

4. Specify connectives between atoms of each group and construct corresponding formulas.

5. Divide formulas and/or any of the remaining atoms of the same level into groups. If there are no groups go to step 7

6. Specify connectives between elements of each group

7. Specify quantifers for the variables.

8. Construct final FOL formula.

### Finding the predicates

**From Jurafsky: 15.4 "Event and State Representation"**

1. Events are captured with predicates that take single event variable as an argument. Events are denoted by verbs.
2. There is no need to specifiy a fixed number of arguments for a given FOL predicate:  as many roles and fillers can be glued on
3. No more roles are postulated than are mentioned in input.
4. The logical connections between closely related inputs that share same predicate are satisfied without the need for additional inference.
5. Syntactic arguments form the arguments of semantic predicates.

Verbs - denote relations between events
Syntactic arguments form the arguments of semantic predicates.

### Data read from AMR representation

#### Sentence

Brutus stabs Caesar with a knife.

#### Parse Graph

```
(s / stab-01
   :ARG0 (p / person
            :name (n / name
                     :op1 "Brutus"))
   :ARG1 (p2 / person
             :name (n2 / name
                       :op1 "Caesar"))
   :instrument (k / knife))
```

#### Instances (6)

Concept relations

```
Instance(source='s', role=':instance', target='stab-01')
Instance(source='p', role=':instance', target='person')
Instance(source='n', role=':instance', target='name')
Instance(source='p2', role=':instance', target='person')
Instance(source='n2', role=':instance', target='name')
Instance(source='k', role=':instance', target='knife')
```

#### Edges 5

Relations between nodes

```
Edge(source='s', role=':ARG0', target='p')
Edge(source='p', role=':name', target='n')
Edge(source='s', role=':ARG1', target='p2')
Edge(source='p2', role=':name', target='n2')
Edge(source='s', role=':instrument', target='k')
```

#### Attributes(2)

Relations between a node and a constant. 

```
Attribute(source='n', role=':op1', target='"Brutus"')
Attribute(source='n2', role=':op1', target='"Caesar"')
```

#### Variables 6

{'n2', 'p2', 'k', 'p', 'n', 's'}

#### Raw Triples 13

```
('s', ':instance', 'stab-01')
('s', ':ARG0', 'p')
('p', ':instance', 'person')
('p', ':name', 'n')
('n', ':instance', 'name')
('n', ':op1', '"Brutus"')
('s', ':ARG1', 'p2')
('p2', ':instance', 'person')
('p2', ':name', 'n2')
('n2', ':instance', 'name')
('n2', ':op1', '"Caesar"')
('s', ':instrument', 'k')
('k', ':instance', 'knife')
```



# Example PropBank role handling

**propbank.py** is the file for making propbank connections. There we fetch the frame for "stab-01"

ARG0 -> 0: stabber
ARG1 -> 1: thing stabbed
ARG2 -> 2: sharp objcect
ARG3 -> 3: specific location of the wound

**TODO** map propbank roles to AMR graph



## Example Parse Result

```
#snt Brutus stabs Caesar with a knife.

[
	["stab-01", "S", "P", "P2", "K"], "&", 
	["person", "P"], "&", 
	["person", "P2"], "&", 
	["knife", "K"], "&", 
	["agent", "S", "P"], "&", 
	["name", "P", "brutus"], "&", 
	["patient", "S", "P2"], "&", 
	["name", "P2", "caesar"], "&", 
	["instrument", "S", "K"]
]

stab-01(S) & agent(S,P) & patient(S,P) & instrument(S, knife) & person(P)& person(P2) & name(P, "brutus") & name(P2, "caesar") 

```



```
# snt: A man opens the door.
(o / open-01 :ARG0 (m / man) :ARG1 (d / door))

open-o1(evt) & :ARG0(evt, man) & ARG1()
open-01(evt) & agent(evt, man) & patient(evt, door)

```





# Aspects of Meaning

* Anaphora resolution - out of scope for now

* List resolution

* Logical connectives resolution

  

