from pathlib import Path


def get_ranges_from_line(line: str) -> list[str]:
    return line.strip().split(",")


def is_invalid(i: int) -> bool:
    i_str = str(i)
    n_half, rem = divmod(len(i_str), 2)
    if rem != 0:
        return False
    if i_str[:n_half] != i_str[n_half:]:
        return False
    return True


def main(filename: str):
    file_path = Path(__file__).parent / filename
    with open(file_path) as file:
        data = file.read()
    ranges = get_ranges_from_line(data)
    invalid = 0
    for pair in ranges:
        start, end = pair.split("-")
        print(start, end)
        for i in range(int(start), int(end) + 1):
            if is_invalid(i):
                print(i)
                invalid += i
    print(f"Invalid ID sum: {invalid}")
    return None


if __name__ == "__main__":
    filename: str = "example-input.txt"
    filename: str = "real-input.txt"
    main(filename)
