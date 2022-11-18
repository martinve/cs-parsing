# Methodology



For constructing the experiment, the following methodology was used:

During the preliminary phase a literature survey was conducted to identify the current state-of-the art in semantic representations of text. Initial experiments were conducted to evaluate the viability of said parsers based on the preliminary survey.

Inputs and outputs were chosen for said system: Given a passage in English, syntactic and semantic information is being extracted and transformed to clauses JSON-LD-LOGIC. 

As a result the parsers and models were chosen: AMR for semantic representation and UD for syntactic and dependency parse trees. As both AMR and UD use sentence as a unit of meaning, a context was constructed that refers to the whole discourse.

For constructing the discourse three classes of  sentences were identified: conceptual, that do not describe specific situations but general concepts; factual that describe named entities and situational - describing concrete situations. A dictionary was constructed to map PropBank roles to 







