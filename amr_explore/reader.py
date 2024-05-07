

if __name__ == "__main__":
    f = open("amr_dict_terms.txt", "r")
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line.endswith("-91"):
            print(line)

    f.close()