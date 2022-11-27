from datasets import load_dataset

"""
Download and save as plain text file Winograd WSC273 dataset
"""

winograd = load_dataset("winograd_wsc", 'wsc273')
data = winograd["test"]

with open("../winograd.txt", "w") as f:
    k = 0
    for it in data:
        f.write(it["text"])
        f.write("\n")
        k += 1
    print(f"Wrote {k} sentences")
