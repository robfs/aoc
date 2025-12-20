from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from pprint import pprint


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


def convert_data_to_coords(data: list[str]) -> list[Coord]:
    xys = map(lambda x: x.split(",", 2), data)
    return [Coord(int(x), int(y)) for x, y in xys]


def create_empty_grid(n_rows: int, n_cols: int) -> list[list[str]]:
    return [["."] * n_cols for _ in range(n_rows)]


def print_grid(grid: list[list[str]]) -> None:
    for row in grid:
        for char in row:
            print(char, end="")
        print()


def add_corner_to_grid(grid: list[list[str]], coord: Coord):
    grid[coord.y][coord.x] = "#"


def calculate_area(coords: tuple[Coord, Coord]) -> tuple[tuple[Coord, Coord], int]:
    a, b = coords
    return coords, (abs(a.x - b.x) + 1) * (abs(a.y - b.y) + 1)


def main(filename: str) -> None:
    filepath = Path(__file__).parent / filename

    with open(filepath) as f:
        data = f.read().splitlines()

    coords = convert_data_to_coords(data)
    print(f"Processing {len(coords)}")
    max_x = max(map(lambda x: x.x, coords))
    max_y = max(map(lambda x: x.y, coords))
    # grid = create_empty_grid(max_y + 2, max_x + 2)
    # for coord in coords:
    #     add_corner_to_grid(grid, coord)
    pairs = combinations(coords, 2)
    # print_grid(grid)

    print("Calculating areas")
    areas = list(map(calculate_area, pairs))
    print(f"{len(areas)} to process")
    areas = sorted(areas, key=lambda x: x[1], reverse=True)
    print(f"Largest area = {areas[0]}")


if __name__ == "__main__":
    filename: str = "example-input.txt"
    filename = "real-input.txt"
    main(filename)
