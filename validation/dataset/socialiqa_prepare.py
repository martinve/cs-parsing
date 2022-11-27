import json

sents = []

out = open("../socialiqa.txt", "w")
inp = open("socialiqa-dev.jsonl")

lines = inp.readlines()
for row in lines:
    data = json.loads(row)
    sent = data["context"]
    out.write(sent)
    out.write("\n")
    print(sent)