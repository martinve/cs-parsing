## Alogrithm for Question Answering

## true / false:
    is john a man?
    are elephants big?
      
    john is a man? Elephants are big?

statement that has ? and no question words

väide seal sees
John is a man. isa(john, man)
Elephants are big. isa(X, elephant) => property(big, X)

@Question isa(john, man) (DB => question)
@Question: [isa(X,elephant) => property(big,X)]
    -> tõestaja püüab leida väärtusi kõikidee Xidele: 

Exists X [isa(X, elephants)]


https://imgur.com/0A0FRck.png

iga alati kehtiva asja jaoks tuleb uus konstant

- tuleb leiutada uus konstant
- suva const jaoks kehtib see asi

Küsimused:
    - lihtsad aatomid ja järeluded

    GKle ei meeldi disjunktsioonid.

Vaja leiutada uus predikaat, defineerida uue reegli

https://imgur.com/hAV46Jq.png, pole isegi vaja konjunktsioone. 

MUUTUJAID EI OLE. Konjuktsioonid ok-d küsimuses.

## Otsime mingit asja küsimus

Who is a man?

a. Leiutame uue nime: Dummy_John

Dummy_John is man. isa(Dummy_John, man)
@Question: isa(?X, man)

https://imgur.com/wslD2uu.png

## Otsime omaduse järgi

https://imgur.com/gP9TDYe.png

## Kuidas teha mingit asja:

Blocks world

Kehtib mignis olukorras. Tegevus mis selleni viib


Our system can answer three kinds of questions:

- Questions that answer yes/no based on the generated KB.
- questions that return the object based on a property.
- Questions returning t


---

From Tammet (16.02)

- true / false:



- is John a man? are elephants big?
- John is a man? Elephants are big?
- Is it true, that John is a man?
- Does it hold that John is a man?



Väide seal sees:
John is a man. isa(john,man)
John is a big man. isa(john,man) & property(big,john)
Elephants are big. Forall X . [isa(X,elephant) => property(big,X)]




@Question: isa(john,man) (DB => question) vastuolu?(DB & -question)
@Question: [isa(c12,elephant) => property(big,c12)] (DB => Forall x. question(x))
[-isa(c12,elephant) V property(big,c12)]



pred12(c12) <=> [isa(c12,elephant) => property(big,c12)]
@Question: pred12(c12)
Question: isa(john,man) & property(big,john)



- "Otsime mingit asja" küsimus:



Who is a man?



Dummy_John is a man. isa(Dummy_John,man)
@Question: isa(?X,man)



Who is a big man? isa(Dummy_John,man) & property(big,Dummy_John)
Question: isa(?X,man) & property(big,?X)



- "Otsime mingit omadust" küsimus:



What color has John?



John has color dummy_red?
property(dummy_red,John) & isa(dummy_red,color)



Question: property(?X,Dummy_John) & isa(?X,color)



- "Kuidas teha mingit asja?"



Blocks world näitel.