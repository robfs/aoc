import random
from pathlib import Path
from pprint import pprint
from typing import Literal, TypeVar

import numpy as np

type Row = int
type Column = int
type Direction = Literal["D", "L", "R"]
type Step = tuple[Row, Column, Direction]
type Timeline = list[Step]


def create_array(data: list[str]) -> np.ndarray:
    arrs = []
    for row in data:
        arr_1 = np.array(list(row), dtype=np.str_)
        arrs.append(arr_1)
    return np.array(arrs)


def get_splitter_locs(data: np.ndarray) -> dict[Row, list[Column]]:
    splitter_locs: dict[Row, list[Column]] = {}

    for row_loc, column_loc in zip(*np.where(data == "^")):
        splitter_locs.setdefault(row_loc, [])
        splitter_locs[row_loc].append(column_loc)

    return splitter_locs


def add_left_step(timeline: Timeline, row: Row, column: Column) -> None:
    step: Step = (row, column - 1, "L")
    timeline.append(step)


def add_right_step(timeline: Timeline, row: Row, column: Column) -> None:
    step: Step = (row, column + 1, "R")
    timeline.append(step)


def create_all_timelines(data: np.ndarray) -> list[Timeline]:
    starting_rows, starting_columns = np.where(data == "S")
    starting_row, starting_column = starting_rows[0], starting_columns[0]
    splitter_locs = get_splitter_locs(data)
    timelines: list[Timeline] = [[(starting_row, starting_column, "D")]]

    for split_row, split_cols in splitter_locs.items():
        new_timelines: list[Timeline] = []
        print(
            f"Processing splits at row {int(split_row)} with {len(timelines):,.0f} timelines."
        )
        for left_timeline in timelines:
            last_step: Step = left_timeline[-1]
            row, column, direction = last_step
            column_found: bool = False
            for split_col in split_cols:
                if column != split_col:
                    continue
                column_found = True
                right_timeline = left_timeline.copy()
                add_left_step(left_timeline, split_row, split_col)
                add_right_step(right_timeline, split_row, split_col)
                new_timelines.append(right_timeline)
            if not column_found:
                new_step: Step = (split_row, column, "D")
                left_timeline.append(new_step)

        print(f"Adding {len(new_timelines):,.0f} new timelines.")
        timelines += new_timelines

    return timelines


def print_array(data: np.ndarray) -> None:
    for row in data:
        for char in row:
            print(char, end="")
        print("")


def draw_timeline(data: np.ndarray, timeline: Timeline) -> None:
    new_data = data.copy()
    for step in timeline:
        row, column, direction = step
        new_data[row, column] = "|"

    print_array(new_data)


def main(fileanme: str) -> None:
    filepath = Path(__file__).parent / filename

    with open(filepath) as f:
        raw_data = f.read().splitlines()

    data = create_array(raw_data)
    timelines = create_all_timelines(data)
    # for timeline in timelines:
    #     draw_timeline(data, timeline)
    print(f"Found {len(timelines)} timelines")


if __name__ == "__main__":
    filename: str = "example-input.txt"
    filename = "real-input.txt"
    main(filename)
