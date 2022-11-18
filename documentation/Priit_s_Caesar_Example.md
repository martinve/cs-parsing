# Priit's Caesar Example

**Input**

Brutus and Caesar are in the curia. Brutus wears a toga. Caesar compliments Brutus on something. Something stabs Caesar.

**Questions**
What does Caesar compliment? What stabs Caesar?

**Commonsense **
Brutus and Caesar are Romans. Toga is clothing. Clothing is where the wearer is. Clothing can be complimented. Clothing cannot stab. Romans can stab. 



## Manually Derived Data

**Open-Text Facts**

For some event e1, 
	e1 is being, and 
	the subject? of e1 is Brutus, and
	the subject? of e1 is Caesar, and
	the location of e1 is curia.

For some event e2
	e2 is wearing, and
	the subject of e2 is Brutus, and 	
	the object of e2 is toga. 

For some event e3
	e3 is complimenting, and
	the subject of e3 is Caesar, and
	the object of e3 is Brutus, and
    complimenting e3 on **something1**

For some event e4
	e4 is stabbing, and
	the subject of e4 is **something**2, and
	the object of e4 is Caesar.

**The events are described in format: `event(e1, stab) & subject(e1,brutus) & subject(e1,caesar).**




```
event(e1, stab).
subject(e1,brutus).
subject(e1,caesar).
location(e1,curia).

# mapping: in ~>

event(e2,wear).
subject(e2, brutus).
object(e2,toga).

event(e3,compliment).
subject(e3,caesar).
object(e3,brutus).
on(e3,something1).

event(e4, stab).
subject(e4,something2).
object(e4,caesar).


//Questions
//what does Caesar compliment?

Pre requisites: 
(blocker) Caesar cannot compliment people, as otherwise the question is not satisfiable.


canstab(X, X), confidence 0.1


//What stabs Caesar?
```


![](https://imgur.com/HXUTY47.png), see also: https://imgur.com/D4g9dcv.png 


### Adding stabber

1. We must find a way to limit 'stabber' to those who are in the room. Possible actors: Brutus, Caesar, toga.



```
{"@question": ["stab","e4","subject"]}
```


# Questions



* `event(e1, stab) & subject(e1,brutus) & subject(e1,caesar).` vs

* `stab(brutus, caesar)` vs 

* `stab-01(brutus, caesar)`

  

How to get correct number of arguments and argument order for stab-01. @see also: http://verbs.colorado.edu/propbank/framesets-english-aliases/stab.html

`(s / stab-01 :ARG0 (s2 / somebody) :ARG1 (p / person :name (n / name :op1 "Caesar")))`

`(s / stab-01 stabber(s2 / somebody) victim(p / person :name (n / name :op1 "Caesar")))`

`(s / stab-01 agent(s2 / somebody) patient(p / person :name (n / name :op1 "Caesar")))`








**Auto Converted via GKC**

```
[

["event","e1","stab"],
["subject","e1","brutus"],
["subject","e1","caesar"],
["location","e1","curia"],

["event","e2","wear"],
["subject","e2","brutus"],
["object","e2","toga"],

["event","e3","compliment"],
["subject","e3","caesar"],
["object","e3","brutus"],
["on","e3","?:X1"],

["event","e4","stab"],
["subject","e4","?:X2"],
["object","e4","caesar"]
]
```





**Auto Generated AMR**

```
(p / person :mod (c / country :name (n / name :op1 "Roman")) :domain (a / and :op1 (p2 / person :name (n2 / name :op1 "Brutus")) :op2 (p3 / person :name (n3 / name :op1 "Caesar"))))
(c / clothing :domain (t / toga))
(c / clothing :location (l / location :location-of (p / person :ARG0-of (w / wear-01))))
(p / possible-01 :ARG1 (c / compliment-01 :ARG1 (c2 / clothing)))
(p / possible-01 :polarity - :ARG1 (s / stab-01 :ARG0 (c / clothing)))
(p / possible-01 :ARG1 (s / stab-01 :ARG0 (p2 / person :mod (c / country :name (n / name :op1 "Romania")))))
```







**rAuto Generated Logical Forms**

```
exists p.(person(p) & exists c.(country(c) & exists n.(name(n) & op1(n,"Roman") & name(c,n)) & mod(p,c)) & exists a.(AND(a) & exists p2.(person(p2) & exists n2.(name(n2) & op1(n2,"Brutus") & name(p2,n2)) & op1(a,p2)) & exists p3.(person(p3) & exists n3.(name(n3) & op1(n3,"Caesar") & name(p3,n3)) & op2(a,p3)) & domain(p,a)))
exists c.(clothing(c) & exists t.(toga(t) & domain(c,t)))
exists c.(clothing(c) & exists l.(location(l) & exists p.(person(p) & exists w.(wear_01(w) & ARG0_of(p,w)) & location_of(l,p)) & location(c,l)))
exists p.(possible_01(p) & exists c.(compliment_01(c) & exists c2.(clothing(c2) & ARG1(c,c2)) & ARG1(p,c)))
-exists p.(possible_01(p) & exists s.(stab_01(s) & exists c.(clothing(c) & ARG0(s,c)) & ARG1(p,s)))
exists p.(possible_01(p) & exists s.(stab_01(s) & exists p2.(person(p2) & exists c.(country(c) & exists n.(name(n) & op1(n,"Romania") & name(c,n)) & mod(p2,c)) & ARG0(s,p2)) & ARG1(p,s)))
```

**Slightly Simplified Auto-Version**

```?
(person(p) & (country(c) & (name(n) & op1(n,"Roman") & name(c,n)) & mod(p,c)) & (AND(a) & .(person(p2) & .(name(n2) & op1(n2,"Brutus") & name(p2,n2)) & op1(a,p2)) & .(person(p3) & .(name(n3) & op1(n3,"Caesar") & name(p3,n3)) & op2(a,p3)) & domain(p,a)))
(clothing(c) & (toga(t) & domain(c,t)))
(clothing(c) & (location(l) & (person(p) & (wear_01(w) & agent_of(p,w)) & location_of(l,p)) & location(c,l)))
(possible_01(p) & (compliment_01(c) & .(clothing(c2) & patient(c,c2)) & patient(p,c)))
-(possible_01(p) & (stab_01(s) & (clothing(c) & agent(s,c)) & patient(p,s)))
(possible_01(p) & (stab_01(s) & .(person(p2) & (country(c) & (name(n) & op1(n,"Romania") & name(c,n)) & mod(p2,c)) & agent(s,p2)) & patient(p,s)))
```

**?Skolemized? Version**

We do not need existential quantifiers, as they 

(`python3 amr2fol2.py Notes_14.txt`)

```
(person(p) & country(c) & name(n) & op1(n,"Roman") & name(c,n) & mod(p,c) & AND(a) & person(p2) & name(n2) & op1(n2,"Brutus") & name(p2,n2) & op1(a,p2) & person(p3) & name(n3) & op1(n3,"Caesar") & name(p3,n3) & op2(a,p3) & domain(p,a))
(clothing(c) & toga(t) & domain(c,t))
(clothing(c) & location(l) & person(p) & wear_01(w) & ARG0_of(p,w) & location_of(l,p) & location(c,l))
(possible_01(p) & compliment_01(c) & clothing(c2) & ARG1(c,c2) & ARG1(p,c))
-(possible_01(p) & stab_01(s) & clothing(c) & ARG0(s,c) & ARG1(p,s))
(possible_01(p) & stab_01(s) & person(p2) & country(c) & name(n) & op1(n,"Romania") & name(c,n) & mod(p2,c) & ARG0(s,p2) & ARG1(p,s))
```

