import re
from pathlib import Path

INVALID = re.compile(r"^(\d+)(\1+)$")


def get_ranges_from_line(line: str) -> list[str]:
    return line.strip().split(",")


def is_invalid(i: int) -> bool:
    i_str = str(i)
    if INVALID.search(i_str):
        print(i_str)
        return True
    return False


def main(filename: str):
    file_path = Path(__file__).parent / filename
    with open(file_path) as file:
        data = file.read()
    ranges = get_ranges_from_line(data)
    invalid = 0
    for pair in ranges:
        start, end = pair.split("-")
        for i in range(int(start), int(end) + 1):
            if is_invalid(i):
                # print(i)
                invalid += i
    print(f"Invalid ID sum: {invalid}")
    return None


if __name__ == "__main__":
    filename: str = "example-input.txt"
    filename: str = "real-input.txt"
    main(filename)
