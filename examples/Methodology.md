# Methodology 

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



# Special phenomena

1. Anaphora resolution - out of scope for now
2. List resolution

3. Logical connectives resolution





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
	["stab-01", "s", "p", "p2", "k"], "&", 
	["person", "p"], "&", 
	["person", "p2"], "&", 
	["knife", "k"], "&", 
	["agent", "s", "p"], "&", 
	["name", "p", "brutus"], "&", 
	["patient", "s", "p2"], "&", 
	["name", "p2", "caesar"], "&", 
	["instrument", "s", "k"]
]

stab-01(s) & agent(s,p) & patient(s,p) & instrument(s, knife) & person(p)& person(p2) & name(p, "brutus") & name(p2, "caesar") 

```



```
# snt: A man opens the door.
(o / open-01 :ARG0 (m / man) :ARG1 (d / door))

open-o1(evt) & :ARG0(evt, man) & ARG1()
open-01(evt) & agent(evt, man) & patient(evt, door)

```




