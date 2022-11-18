# nlpsolver examples

## Not working

"Mike is good and strong and a car is nice. Eve is also strong. All red elephants are not strong. Robert is not strong. Who is not strong?"
Error: prover output is not a correct json

Fixed partially, but not for 
"An animal is young or adult." like in
"Elephants have trunks. Young elephants are small, adult elephants are big. Elephants are animals. Animals are young or adult. If an animal is young, it is not adult. Mike is a young animal. Mike is adult?"

"Elephants have trunks. Young elephants are small, adult elephants are big. Elephants are animals. Animals are young or adult. If an animal is young, it is not adult. Mike is a young elephant. Who is small?"
Some Young elephant.

Fixed:
"Penguins are birds. Birds can fly. Mike is a bird. Mike can fly?"
Did not understand an input sentence:                     Birds can fly.

"Penguins are birds. Birds are red. Penguins are not red. Mike is a bird. John is a penguin. John is red?"
True.

"Penguins are birds. Birds are red. No penguin is red. Mike is a bird. John is a penguin. John is red?"
True.

"Sparrows are birds. Birds are red. Sparrows are not red. Mike is a bird. John is a sparrow. Who is red?"
Error: prover output is not a correct json

Fixed:
"Persons are humans. Mike is a human?"
Could not find an answer.