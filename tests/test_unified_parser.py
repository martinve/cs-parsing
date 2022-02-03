import os

from server.unified_parser import get_constituency


if __name__ == "__main__":
    print(os.getcwd())

    snt = "All cats are animals"

    const = get_constituency(snt)
    print(const)
