from dataclasses import dataclass, field
from itertools import combinations, pairwise
from pathlib import Path
from typing import Literal, Self


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    @classmethod
    def from_tuple(cls, coords: tuple[int, int]) -> Self:
        return cls(*coords)


@dataclass(frozen=True)
class Line:
    a: Coord
    b: Coord

    @classmethod
    def from_tuple(cls, coords: tuple[Coord, Coord]) -> Self:
        return cls(*coords)

    @property
    def coords(self) -> tuple[Coord, Coord]:
        a, b = self.a, self.b
        if self.direction() == "H":
            if b.x < a.x:
                a, b = b, a
            return a, b
        else:
            if b.y < a.y:
                a, b = b, a
            return a, b

    def direction(self) -> Literal["H", "V"]:
        if self.a.x == self.b.x:
            return "V"
        elif self.a.y == self.b.y:
            return "H"
        else:
            raise ValueError("Invalid Line")


@dataclass(frozen=True)
class Rectangle:
    _corners: tuple[Coord, Coord]

    @property
    def min_x(self) -> int:
        a, b = self._corners
        return min(a.x, b.x)

    @property
    def min_y(self) -> int:
        a, b = self._corners
        return min(a.y, b.y)

    @property
    def max_x(self) -> int:
        a, b = self._corners
        return max(a.x, b.x)

    @property
    def max_y(self) -> int:
        a, b = self._corners
        return max(a.y, b.y)

    @property
    def top_left(self) -> Coord:
        return Coord(self.min_x, self.min_y)

    @property
    def top_right(self) -> Coord:
        return Coord(self.max_x, self.min_y)

    @property
    def bottom_right(self) -> Coord:
        return Coord(self.max_x, self.max_y)

    @property
    def bottom_left(self) -> Coord:
        return Coord(self.min_x, self.max_y)

    @property
    def corners(self) -> tuple[Coord, Coord, Coord, Coord]:
        return self.top_left, self.top_right, self.bottom_right, self.bottom_left

    @property
    def edges(self) -> tuple[Line, Line, Line, Line]:
        top = Line(self.top_left, self.top_right)
        right = Line(self.top_right, self.bottom_right)
        bottom = Line(self.bottom_left, self.bottom_right)
        left = Line(self.top_left, self.bottom_left)
        return top, right, bottom, left

    @property
    def area(self) -> int:
        x = self.max_x - self.min_x + 1
        y = self.max_y - self.min_y + 1
        return x * y


@dataclass
class Grid:
    _corners: list[Coord]
    scale: int = 1
    _max_x: int = 0
    _max_scaled_x: int = 0
    _max_y: int = 0
    _max_scaled_y: int = 0
    _scaled_corners: list[Coord] = field(default_factory=list)
    _grid: list[str] = field(default_factory=list)
    _scaled_grid: list[str] = field(default_factory=list)

    def corners(self, scaled: bool = False) -> list[Coord]:
        if not scaled:
            return self._corners
        if self._scaled_corners:
            return self._scaled_corners
        corners: list[Coord] = []
        for corner in self._corners:
            scaled_corner = Coord(corner.x // self.scale, corner.y // self.scale)
            if scaled_corner not in corners:
                corners.append(scaled_corner)
        self._scaled_corners = corners
        return self._scaled_corners

    def rectangles(self, scaled: bool = False) -> list[Rectangle]:
        combos = combinations(self.corners(scaled), 2)
        return list(map(Rectangle, combos))

    def max_x(self, scaled: bool = False) -> int:
        if not self._max_x:
            self._max_x = max(corner.x for corner in self.corners(False))
        if not self._max_scaled_x:
            self._max_scaled_x = max(corner.x for corner in self.corners(True))
        if scaled:
            return self._max_scaled_x
        return self._max_x

    def max_y(self, scaled: bool = False) -> int:
        if not self._max_y:
            self._max_y = max(corner.y for corner in self.corners(False))
        if not self._max_scaled_y:
            self._max_scaled_y = max(corner.y for corner in self.corners(True))
        if scaled:
            return self._max_scaled_y
        return self._max_y

    def init_grid(self, scaled: bool = False) -> list[str]:
        ny = self.max_y(scaled) + 2
        nx = self.max_x(scaled) + 2
        print(f"\tInitialising the grid of {ny:,.0f} rows and {nx:,.0f} columns")
        blank_line = "." * nx
        grid = [blank_line for _ in range(ny)]
        edges = self.edges(scaled)
        verticals = [edge for edge in edges if edge.direction() == "V"]
        for i in range(ny):
            print(f"\t\tFilling row {i + 1:,.0f}/{ny:,.0f} of the grid")
            relevant_edges: list[Line] = []
            for edge in verticals:
                a, b = edge.coords
                if not a.y <= i <= b.y:
                    continue
                relevant_edges.append(edge)
            if not relevant_edges:
                continue
            min_x = min(map(lambda edge: edge.a.x, relevant_edges))
            max_x = max(map(lambda edge: edge.a.x, relevant_edges))
            row = "." * (min_x - 1)
            row += "X" * (max_x - min_x + 1)
            row += "." * (nx - max_x)
            grid[i] = row
        return grid

    def grid(self, scaled: bool = False) -> list[str]:
        if not self._grid:
            self._grid = self.init_grid(False)
            return self._grid
        if not self._scaled_grid:
            self._scaled_grid = self.init_grid(True)
        return self._scaled_grid if scaled else self._grid

    def print_grid(self, grid: list[str] | None = None) -> None:
        if grid is None:
            grid = self.grid(True)
        print()
        for row in grid:
            print(row)

    def edges(self, scaled: bool = False) -> list[Line]:
        corners = self.corners(scaled)
        corners.append(corners[0])
        edge_ends = pairwise(corners)
        return list(map(Line.from_tuple, edge_ends))

    def print_rectangle(self, rectangle: Rectangle) -> None:
        grid = self.init_grid(True)
        for i in range(rectangle.min_y, rectangle.max_y + 1):
            row = grid[i]
            n_chars = len(row)
            row = "." * (rectangle.min_x - 1)
            row += "O" * (rectangle.max_x - rectangle.min_x + 1)
            row += "." * (n_chars - rectangle.max_x)
        self.print_grid(grid)

    def is_rectangle_valid(self, rectangle: Rectangle, scaled: bool = False) -> bool:
        tl, tr, _, bl = rectangle.corners
        min_x, max_x, min_y, max_y = tl.x, tr.x, tl.y, bl.y
        grid = self.grid(scaled)
        for i in range(min_y, max_y + 1):
            if not (grid[i][min_x] == "X" and grid[i][max_x] == "X"):
                return False
            if i == min_y or i == max_y:
                if not all([cell == "X" for cell in grid[i][min_x : max_x + 1]]):
                    return False
        for i, row in enumerate(grid[min_y : max_y + 1]):
            if not all([cell == "X" for cell in row[min_x : max_x + 1]]):
                return False
        return True


def main(filename: str) -> None:
    filepath = Path(__file__).parent / filename

    with open(filepath) as f:
        data: list[str] = f.read().splitlines()

    xys = map(lambda row: tuple(map(int, row.split(",", 2))), data)
    coords = map(Coord.from_tuple, xys)
    scale = 200 if filename == "real-input.txt" else 1
    grid = Grid(list(coords), scale)
    max_area = 0

    scaled: bool = False
    rectangles = grid.rectangles(scaled)
    for i, rectangle in enumerate(grid.rectangles(scaled), 1):
        if rectangle.area <= max_area:
            print(
                f"Skipping rectangle {i:,.0f}/{len(rectangles):,.0f} of area {rectangle.area:,.0f}"
            )
            continue
        print(
            f"Checking rectangle {i:,.0f}/{len(rectangles):,.0f} of area {rectangle.area:,.0f}"
        )
        if grid.is_rectangle_valid(rectangle, scaled):
            print(f"Found valid rectangle with area {rectangle.area:,.0f}")
            max_area = rectangle.area

    print(f"Max total area = {max_area}")


if __name__ == "__main__":
    filename: str = "example-input.txt"
    filename = "real-input.txt"
    main(filename)
