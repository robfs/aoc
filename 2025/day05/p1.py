from pathlib import Path


def main(filename: str) -> None:
    filepath = Path(__file__).parent / filename
    with open(filepath) as f:
        data = f.read()
    raw_ranges, raw_ids = data.split("\n\n")
    ranges = raw_ranges.splitlines()
    ids = map(int, raw_ids.splitlines())
    n_fresh = 0
    for id_ in ids:
        for range_ in ranges:
            start, end = tuple(map(int, range_.split("-")))
            if start <= id_ <= end:
                n_fresh += 1
                break
    print(f"Number of fresh IDs: {n_fresh}")
    return None


if __name__ == "__main__":
    filename: str = "example-input.txt"
    filename = "real-input.txt"
    main(filename)
