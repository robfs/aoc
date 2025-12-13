from pathlib import Path

import numpy as np


def create_array(data: list[str]) -> np.ndarray:
    arrs = []
    for row in data:
        arr_1 = np.array(list(row), dtype=np.str_)
        arrs.append(arr_1)
    return np.array(arrs)


def check_neighbours(arr: np.ndarray, y: int, x: int) -> bool:
    full_neighbours = 0
    for y_ in [y - 1, y, y + 1]:
        if not (0 <= y_ < arr.shape[0]):
            continue
        for x_ in [x - 1, x, x + 1]:
            if not (0 <= x_ < arr.shape[1]):
                continue
            if (y_ == y) and (x_ == x):
                continue
            if arr[y_, x_] == "@":
                full_neighbours += 1
    return full_neighbours < 4


def main(filename: str) -> None:
    file_path = Path(__file__).parent / filename
    with open(file_path) as f:
        data = f.read().splitlines()
    arr = create_array(data)
    new_arr = arr.copy()

    total = 0
    n_available = 1
    while n_available > 0:
        n_available = 0
        for y in range(arr.shape[0]):
            for x in range(arr.shape[1]):
                if not arr[y, x] == "@":
                    continue
                if check_neighbours(arr, y, x):
                    new_arr[y, x] = "x"
                    n_available += 1
        total += n_available
        print(f"Removed {n_available} rolls")
        arr = new_arr.copy()

    print(f"Total removed: {total}")

    return None


if __name__ == "__main__":
    filename: str = "example-input.txt"
    filename = "real-input.txt"
    main(filename)
