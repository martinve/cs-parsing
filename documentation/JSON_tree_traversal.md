# JSON tree traversal

## Example 1

Given sentence `Brutus stabs Caesar with a knife`

We will have an AMR graph:

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

And this transformed to JSON array

```
[
	['s', 'stab-01'],
 	[':ARG0', 
 		['p', 'person'], 
 		[':name', ['n', 'name'], [':op1', 'Brutus']]],
 	[':ARG1', 
 		['p2', 'person'], 
 		[':name', ['n2', 'name'], [':op1', 'Caesar']]],
 	[':instrument', ['k', 'knife']]
 ]
```

Now we want to transform this to logical form



## Example 2 

Given sentence ` Donald Trump was a president of the United States of America.`

```
(h / have-org-role-91
      :ARG0 (p / person
            :name (n / name
                  :op1 "Donald"
                  :op2 "Trump"))
      :ARG1 (c / country
            :name (n2 / name
                  :op1 "United"
                  :op2 "States"
                  :op3 "of"
                  :op4 "America"))
      :ARG2 (p2 / president))
```

The graph is transformed to JSON array

```
[['h', 'have-org-role-91'],
 [':ARG0', ['p', 'person'],
  [':name', ['n', 'name'], [':op1', 'Donald'], [':op2', 'Trump']]],
 [':ARG1', ['c', 'country'],
  [':name', ['n2', 'name'], [':op1', 'United'], [':op2', 'States'],
   [':op3', 'of'], [':op4', 'America']]],
 [':ARG2', ['p2', 'president']]]
```

Now we want to transform this to logical form.

