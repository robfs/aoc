import time
from multiprocessing import Pool
from pathlib import Path
from pprint import pprint
from typing import Literal

import numpy as np

type Row = int
type Column = int
type Direction = Literal["D", "L", "R"]
type Step = tuple[Row, Column, Direction]
type Timeline = str  # "DLRDDLDDLR"


def create_array(data: list[str]) -> np.ndarray:
    arrs = []
    for row in data:
        arr_1 = np.array(list(row), dtype=np.str_)
        arrs.append(arr_1)
    return np.array(arrs)


def get_splitter_locs(data: np.ndarray) -> dict[Row, list[Column]]:
    splitter_locs: dict[Row, list[Column]] = {}

    for row_loc, column_loc in zip(*np.where(data == "^")):
        splitter_locs.setdefault(int(row_loc), [])
        splitter_locs[row_loc].append(int(column_loc))

    return splitter_locs


def add_down_step(timeline: Column) -> Column:
    return timeline


def add_left_step(timeline: Column) -> Column:
    return timeline - 1


def add_right_step(timeline: Column) -> Column:
    return timeline + 1


def create_all_steps(data: np.ndarray) -> dict[Column, int]:
    _, starting_columns = np.where(data == "S")
    starting_column = int(starting_columns[0])
    splitter_locs = get_splitter_locs(data)
    column_timelines: dict[Column, int] = {starting_column: 1}

    for split_row, split_cols in splitter_locs.items():
        new_column_timelines: dict[Column, int] = {}
        for column, n_timelines in column_timelines.items():
            if column not in split_cols:
                _ = new_column_timelines.setdefault(column, 0)
                new_column_timelines[column] += n_timelines

            else:
                _ = new_column_timelines.setdefault(column - 1, 0)
                _ = new_column_timelines.setdefault(column + 1, 0)
                new_column_timelines[column - 1] += n_timelines
                new_column_timelines[column + 1] += n_timelines

            column_timelines = new_column_timelines

        n_timelines = sum(n for n in column_timelines.values())
        print(f"\tAt row {split_row} have {n_timelines:,.0f}")

    return column_timelines


def main(filename: str) -> None:
    filepath = Path(__file__).parent / filename

    with open(filepath) as f:
        raw_data = f.read().splitlines()

    data = create_array(raw_data)
    column_timelines = create_all_steps(data)
    # pprint(column_timelines)
    total = 0
    for timelines in column_timelines.values():
        total += timelines
    print(f"Found {total} timelines")


if __name__ == "__main__":
    filename: str = "example-input.txt"
    filename = "real-input.txt"
    main(filename)
