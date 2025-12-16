from pathlib import Path

import numpy as np


def create_array(data: list[str]) -> np.ndarray:
    arrs = []
    for row in data:
        arr_1 = np.array(list(row), dtype=np.str_)
        arrs.append(arr_1)
    return np.array(arrs)


def process_array(data: np.ndarray) -> np.ndarray:
    max_x, max_y = data.shape
    new_data = data.copy()
    splits = 0
    for y, row in enumerate(new_data):
        if y == max_y:
            break
        for x, char in enumerate(row):
            if char == ".":
                continue
            elif char == "S":
                new_data[y + 1, x] = "|"
            elif char == "|":
                char_below = new_data[y + 1, x]
                if char_below == ".":
                    new_data[y + 1, x] = "|"
                elif char_below == "^":
                    splits += 1
                    new_data[y + 1, x - 1] = "|"
                    new_data[y + 1, x + 1] = "|"

    print(f"Beam split: {splits} times")

    return new_data


def main(fileanme: str) -> None:
    filepath = Path(__file__).parent / filename

    with open(filepath) as f:
        raw_data = f.read().splitlines()

    data = create_array(raw_data)
    new_data = process_array(data)

    print(new_data)


if __name__ == "__main__":
    filename: str = "example-input.txt"
    filename = "real-input.txt"
    main(filename)
