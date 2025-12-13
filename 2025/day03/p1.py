from pathlib import Path


def get_highest_joltage(line: str, n: int = 2) -> int:
    batts = list(map(int, list(line)))
    first_digit = max(batts[: -n + 1])
    first_digit_index = batts.index(first_digit)
    second_digit = max(batts[first_digit_index + 1 :])
    print(batts)
    print(f"{first_digit=} at index {first_digit_index}, {second_digit=}")
    return first_digit * 10 + second_digit


def main(filename: str) -> None:
    file_path = Path(__file__).parent / filename
    total_joltage: int = 0
    with open(file_path) as f:
        data = f.read().splitlines()

    for line in data:
        joltage = get_highest_joltage(line)
        print(line, joltage)
        total_joltage += joltage

    print(f"Total joltage: {total_joltage}")

    return None


if __name__ == "__main__":
    filename: str = "example-input.txt"
    filename = "real-input.txt"
    main(filename)
