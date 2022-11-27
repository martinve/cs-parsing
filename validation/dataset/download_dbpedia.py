from datasets import load_dataset

"""
Download and save as plain text file Winograd WSC273 dataset
"""

ds = load_dataset("dbpedia_14")
data = ds["test"]

with open("../dbpedia.txt", "w") as f:
    k = 0
    for it in data:
        f.write(it["content"])
        f.write("\n")
        k += 1
    print(f"Wrote {k} sentences")
