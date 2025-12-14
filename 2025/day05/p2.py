from pathlib import Path
from pprint import pprint


def sort_ranges(ranges: list[str]) -> list[tuple[int, int]]:
    return sorted(
        map(lambda x: tuple(map(int, x.split("-"))), ranges), key=lambda x: x[0]
    )


def do_ranges_overlap(r1: tuple[int, int], r2: tuple[int, int]) -> bool:
    s1, e1 = r1
    s2, e2 = r2
    return s2 <= e1


def merge_ranges(r1: tuple[int, int], r2: tuple[int, int]) -> tuple[int, int]:
    start = min(r1[0], r2[0])
    end = max(r1[1], r2[1])
    return (start, end)


def main(filename: str) -> None:
    filepath = Path(__file__).parent / filename
    with open(filepath) as f:
        data = f.read()
    raw_ranges, raw_ids = data.split("\n\n")
    ranges = raw_ranges.splitlines()
    n_ranges = len(ranges)
    new_ranges = []

    # Sort ranges
    sorted_ranges = sort_ranges(ranges)
    pprint(sorted_ranges)

    # Load the first value as the merged
    merged = sorted_ranges[0]

    # Initialise i at the second element
    i = 1

    # Iterate through the range
    while i < n_ranges:
        # Get the test value
        to_test = sorted_ranges[i]

        # Start a loop to continue merging until an exclusive pair is found
        while do_ranges_overlap(merged, to_test):
            print(f"{merged} and {to_test} overlap, merging")
            merged = merge_ranges(merged, to_test)

            # Increment i
            i += 1

            # Break if at the end of the ranges
            if i >= n_ranges:
                print("Limit hit")
                break

            # Set to test as the next value
            to_test = sorted_ranges[i]
            print(f"Merged to {merged}, testing against {to_test}")

        # If ranges do not overlap, add previous range to list
        print(f"{merged} and {to_test} are exclusive, adding {merged}")
        new_ranges.append(merged)

        # Set next exclusive range to merged
        merged = to_test

        # Increment i
        i += 1

    # check the last value in the range
    merged = new_ranges[-1]
    to_test = sorted_ranges[-1]
    if not do_ranges_overlap(merged, to_test):
        new_ranges.append(to_test)
    else:
        merged = merge_ranges(merged, to_test)
        new_ranges[-1] = merged

    pprint(new_ranges)
    fresh_ids = sum(len(range(x, y + 1)) for x, y in new_ranges)
    print(f"{fresh_ids} fresh IDs")

    return None


if __name__ == "__main__":
    filename: str = "example-input.txt"
    filename = "real-input.txt"
    main(filename)
