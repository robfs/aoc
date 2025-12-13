from pathlib import Path


def get_highest_joltage(line: str, n: int = 2) -> int:
    batts = list(map(int, list(line)))
    digits = [0] * n
    n_idx = 0
    for i, digit in enumerate(digits):
        end_idx = -n + i
        if i == n - 1:
            available_batts = batts[n_idx:]
        else:
            available_batts = batts[n_idx : -n + i + 1]
        digit = max(available_batts)
        digits[i] = digit
        new_idx = available_batts.index(digit)
        n_idx += new_idx + 1
    return int("".join(map(str, digits)))


def main(filename: str) -> None:
    file_path = Path(__file__).parent / filename
    total_joltage: int = 0
    with open(file_path) as f:
        data = f.read().splitlines()

    for i, line in enumerate(data):
        joltage = get_highest_joltage(line, 12)
        print(line, joltage)
        total_joltage += joltage

    print(f"Total joltage: {total_joltage}")

    return None


if __name__ == "__main__":
    filename: str = "example-input.txt"
    filename = "real-input.txt"
    main(filename)
