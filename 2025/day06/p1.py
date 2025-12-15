from pathlib import Path


def main(filename: str):
    filepath = Path(__file__).parent / filename

    with open(filepath) as f:
        data = f.read().splitlines()

    operators = data[-1].split()
    number_lists = [row.split() for row in data[:-1]]

    total = 0
    for op, *args in zip(operators, *number_lists):
        calc = eval(op.join(args))
        total += calc

    print(f"Total is {total}")


if __name__ == "__main__":
    filename: str = "example-input.txt"
    filename = "real-input.txt"

    main(filename)
