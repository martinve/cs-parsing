passage:

All cats are animals. Mike is a cat. Mike is a an animal?

prover input:
 [ {"@logic": ["instance", "animal", "a"]},
  {"@logic": [":domain", "cat", "c"]},
  {"@logic": [":mod", "all", "a2"]},
  {"@logic": ["instance", "cat", "c"]},
  {"@logic": [":domain", "person", "p"]},
  {"@logic": ["name", "p", "mike"]},
  { "@question": [ ["instance", "animal", "a"],
                   [":polarity", "amr-unknown", "a2"],
                   [":domain", "person", "p"],
                   ["name", "p", "mike"]]}]
prover output:
 {"result": "answer found",

"answers": [
{
"answer": true,
"confidence": 1,
"positive proof":
[
[1, ["in", "frm_7", "goal", 1], [["-:domain","person","p"]]],
[2, ["in", "frm_5", "axiom", 1], [[":domain","person","p"]]],
[3, ["simp", 1, 2, "fromgoal", 1], false]
]}
]}


passage:

All cats are animals. Mike is a cat. Mike is a an animal?

prover input: [ {"@logic": ["instance", "animal", "a"]}, {"@logic": [":domain", "cat", "c"]}, {"@logic": [":mod", "all", "a2"]}, {"@logic": ["instance", "cat", "c"]}, {"@logic": [":domain", "person", "p"]}, {"@logic": ["name", "p", "mike"]}, { "@question": [ ["instance", "animal", "a"], [":polarity", "amr-unknown", "a2"], [":domain", "person", "p"], ["name", "p", "mike"]]}] prover output: {"result": "answer found",

"answers": [ { "answer": true, "confidence": 1, "positive proof": [ [1, ["in", "frm_7", "goal", 1], [["-:domain","person","p"]]], [2, ["in", "frm_5", "axiom", 1], [[":domain","person","p"]]], [3, ["simp", 1, 2, "fromgoal", 1], false] ]} ]}

% general rule instanceof(X, Y) => isa(X, Y). % facts isa(cat, X) => instanceof(animal, X). name(mike, p). instanceof(cat, p). % question -(name(mike, p) & instanceof(animal, p)).

[ [["instanceof","?:X","?:Y"], "=>", ["isa","?:X","?:Y"]], [["isa","cat","?:X"], "=>", ["instanceof","animal","?:X"]], ["name","mike","p"], ["instanceof","cat","p"], ["~", [["name","mike","p"], "&", ["instanceof","animal","p"]]] ]