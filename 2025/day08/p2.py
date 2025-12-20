from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from pprint import pprint


@dataclass(unsafe_hash=True)
class Box:
    x: int
    y: int
    z: int

    def __sub__(self, other: "Box") -> float:
        return (
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        ) ** 0.5


def get_junction_boxes(data: list[str]):
    coords_str: map[list[str]] = map(lambda x: x.split(",", 3), data)
    coords: map[tuple[int, ...]] = map(lambda x: tuple(map(int, x)), coords_str)
    boxes: map[Box] = map(lambda x: Box(*tuple(x)), coords)
    return boxes


def clean_groups(groups: dict[int, set[Box]]) -> dict[int, set[Box]]:
    starting_groups = len(groups)
    new_groups: list[set[Box]] = []
    for group in groups.values():
        found: bool = False
        for i, new_group in enumerate(new_groups):
            if len(group & new_group) > 0:
                new_groups[i] |= group
                found = True
        if not found:
            new_groups.append(group)

    ending_groups = len(new_groups)
    print(f"\t\tReduced groups from {starting_groups} to {ending_groups}")
    return {i: group for i, group in enumerate(new_groups)}


def connect_all_boxes(
    distances: list[tuple[Box, Box]], n_boxes: int
) -> tuple[Box | None, Box | None]:
    i = 0
    connections_made: int = 0
    # Create groups variable to store box links
    groups: dict[int, set[Box]] = {}
    for box1, box2 in distances:
        # print(f"Processing {box1} and {box2}")
        # Process link between box1 and box2
        found: bool = False
        for x, links in groups.items():
            if box1 in links and box2 in links:
                # Both boxes present in a single link already - ignoring
                # print(f"\tIgnoring boxes {box1} and {box2} because already connected")
                # Setting the found variable so new index is not created
                found = True
                continue
            elif box1 in links or box2 in links:
                # One box in an existing link, adding other box to that link
                # print(f"\tAdding {box1} and {box2} to index {x}")
                groups[x] |= {box1, box2}
                # Setting the found variable so new index is not created
                found = True
                break
        if not found:
            # If found did not get set, create a new group and increment index
            # print(f"\tAdding {box1} and {box2} to new index {i}")
            groups[i] = {box1, box2}
            i += 1

        # In case new pair connects other groups, combine
        groups = clean_groups(groups)

        print(
            f"\tHave {len(groups)} with {len(groups[0])} in first index vs. {n_boxes}."
        )
        if len(groups) == 1 and len(groups[0]) == n_boxes:
            return box1, box2
    return None, None


def main(filename: str) -> None:
    filepath = Path(__file__).parent / filename

    with open(filepath) as f:
        data = f.read().splitlines()

    n_boxes = len(data)
    junction_boxes: map[Box] = get_junction_boxes(data)
    combos: combinations[tuple[Box, Box]] = combinations(junction_boxes, 2)
    distances: dict[tuple[Box, Box], float] = {a: a[0] - a[1] for a in combos}
    pairs = [key for key, _ in sorted(distances.items(), key=lambda item: item[1])]
    box1, box2 = connect_all_boxes(pairs, n_boxes)
    if box1 and box2:
        print(f"{box1} and {box2} result in fully linked boxes")
        print(f"Answer = {box1.x * box2.x}")
    else:
        print(f"Failed to link all boxes")


if __name__ == "__main__":
    filename: str = "example-input.txt"
    filename = "real-input.txt"
    main(filename)
