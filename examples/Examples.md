# Examples for GK reasoner

## Baltic flags example

The colors for flag of Lithuania are yellow, green and red. 

0 causer of coloration
1 thing with color
2 the color itself



`(c / color-01 :ARG1 (f / flag :poss (c2 / country :name (n / name :op1 \"Lithuania\"))) :ARG2 (a / and :op1 (y / yellow) :op2 (g / green) :op3 (r / red)))`



**Clauses**

```
[
  ['instance', 'color-01', 'c'],
  ['thing_with_color', 'flag', 'f'],
  ['belongsto', 'country', 'c2'],
  ['name', 'c2', 'lithuania'],
  ['c', 'and', ['yellow', 'green', 'red']]]
]
```

The colors for flag of Latvia are red and white. 

`(a / and :op1 (c / color :mod (r / red)) :op2 (c2 / color :mod (w / white)) :domain (f / flag :poss (c3 / country :name (n / name :op1 \"Lettonia\"))))`

**Hypothes**

The colors for flag of Latvia are red. and white. 



**Clauses**

```
[ ['a', 'and'],
  [':op1', ['c', 'color'], [':mod', ['r', 'red']]],
  [':op2', ['c2', 'color'], [':mod', ['w', 'white']]],
  [ ':domain',
    ['f', 'flag'],
    [ ':poss',
      ['c3', 'country'],
      [':name', ['n', 'name'], [':op1', 'Lettonia']]]]]
```

**Logic**

```
[ ['instance', 'and', 'a'],
  [':op1', 'color', 'c'],
  [':mod', 'red', 'r'],
  [':op2', 'color', 'c2'],
  [':mod', 'white', 'w'],
  [':domain', 'flag', 'f'],
  [':poss', 'country', 'c3'],
  ['name', 'c3', 'lettonia']]
```



The colors for flag of Estonia are blue, black and white.

```
(c / color-01 :ARG1 (f / flag :poss (c2 / country :name (n / name :op1 \"Estonia\"))) :ARG2 (a / and :op1 (b / blue) :op2 (b2 / black-and-white)))"
```



### AMRs


(a / and :op1 (c / color :mod (r / red)) :op2 (c2 / color :mod (w / white)) :domain (f / flag :poss (c3 / country :name (n / name :op1 \"Lettonia\"))))"
(c / color-01 :ARG1 (f / flag :poss (c2 / country :name (n / name :op1 \"Estonia\"))) :ARG2 (a / and :op1 (b / blue) :op2 (b2 / black-and-white)))"
            

### Generated Clauses

```
[ {'@logic': ['instance', 'color-01', 'c']},
  {'@logic': ['patient', 'flag', 'f']},
  {'@logic': [':poss', 'country', 'c2']},
  {'@logic': ['name', 'c2', 'lithuania']},
  {'@logic': ['instrument', 'and', 'a']},
  {'@logic': ['a', [['y', 'yellow'], ['g', 'green'], ['r', 'red']]]},
  {'@logic': ['instance', 'and', 'a']},
  {'@logic': [':op1', 'color', 'c']},
  {'@logic': [':mod', 'red', 'r']},
  {'@logic': [':op2', 'color', 'c2']},
  {'@logic': [':mod', 'white', 'w']},
  {'@logic': [':domain', 'flag', 'f']},
  {'@logic': [':poss', 'country', 'c3']},
  {'@logic': ['name', 'c3', 'lettonia']},
  {'@logic': ['instance', 'color-01', 'c']},
  {'@logic': ['patient', 'flag', 'f']},
  {'@logic': [':poss', 'country', 'c2']},
  {'@logic': ['name', 'c2', 'estonia']},
  {'@logic': ['instrument', 'and', 'a']},
  {'@logic': ['a', [['b', 'blue'], ['b2', 'black-and-white']]]}]
```



# Toy example

```
passage: "All cats are animals. Mike is a cat."
statement": "Mike is an animal".
Q: If passage -> statement (yes, no, proof)

amr = '(s / stab-01 :ARG0 (p / person :name (n / name :op1 "Brutus"))'
::snt A flashlight emits light.
```

```
(a / animal :domain (c / cat :mod (a2 / all)))
(c / cat :domain (p / person :name (n / name :op1 \"Mike\")))
```

```
(a / animal :domain (p / person :name (n / name :op1 "Mike")))
```



---

"All cats are animals. **Mike** is a cat. Is **he** an animal?".







# Clauses





## Kuressaare example

AMR: (a / and :op1 (b / be-located-at-91 :ARG1 (c / city :name (n / name :op1 "Saaremaa")) :ARG2 (c2 / country :name (n2 / name :op1 "Estonia"))) :op2 (b2 / be-located-at-91 :ARG1 (c3 / city :name (n3 / name :op1 "Kuressaare")) :ARG2 c2))



```
(a / and :op1 (b / be-located-at-91 :ARG1 (c / geo :name (n / name :op1 "Saaremaa")) :ARG2 (c2 / geo :name (n2 / name :op1 "Estonia"))) :op2 (b2 / be-located-at-91 :ARG1 (c3 / city :name (n3 / name :op1 "Kuressaare")) :ARG2 c2))
```



## Vinken example

```
 (j / join-01 :ARG0 (p / person :name (n / name :op1 "Pierre" :op2 "Vinken") :age (t / temporal-quantity :quant 61 :unit (y / year))) :ARG1 (b / board) :ARG2 (d / director :mod (e / executive :polarity -)) :time (d2 / date-entity :day 29 :month 11))
```



