import re
from pathlib import Path


def find_breaks(data: list[str]) -> list[int]:
    breaks = set()
    p = re.compile(" ")
    for row in data:
        ms = p.finditer(row)
        space_locs = {m.span()[0] for m in ms}
        if not breaks:
            breaks = space_locs
        else:
            breaks &= space_locs

    return sorted(list(breaks))


def translate_args(args: list[str]) -> list[str]:
    i = max(map(len, args))
    new_args: list[str] = []

    while i >= 0:
        new_arg = ""
        for arg in args:
            try:
                new_arg += arg[i]
            except Exception as e:
                continue

        if new_arg:
            new_args.append(new_arg.strip())
        i -= 1

    return new_args


def main(filename: str):
    filepath = Path(__file__).parent / filename

    with open(filepath) as f:
        data = f.read().splitlines()

    operators = data[-1].split()
    break_locs = find_breaks(data)
    cols = []
    start = 0
    for break_loc in break_locs:
        col = []
        for row in data[:-1]:
            col.append(row[start:break_loc])
        cols.append(col)
        start = break_loc + 1

    col = []

    for row in data[:-1]:
        col.append(row[start:])

    cols.append(col)

    cols = reversed(cols)
    operators = reversed(operators)

    total = 0

    for op, args in zip(operators, cols):
        new_args = translate_args(args)
        calc = op.join(new_args)
        total += eval(calc)

    print(f"Total is {total}")


if __name__ == "__main__":
    filename: str = "example-input.txt"
    filename = "real-input.txt"

    main(filename)
