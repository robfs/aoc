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
    new_groups: list[set[Box]] = []
    for group in groups.values():
        found: bool = False
        for i, new_group in enumerate(new_groups):
            if len(group & new_group) > 0:
                new_groups[i] |= group
                found = True
        if not found:
            new_groups.append(group)

    return {i: group for i, group in enumerate(new_groups)}


def process_distances(
    distances: list[tuple[tuple[Box, Box], float]], n_connections: int
):
    i = 0
    connections_made: int = 0
    groups: dict[int, set[Box]] = {}
    for (box1, box2), distance in distances:
        found: bool = False
        for x, links in groups.items():
            if box1 in links and box2 in links:
                # print(f"Ignoring boxes {box1} and {box2} because already connected")
                continue
            elif box1 in links or box2 in links:
                # print(f"Adding {box1} and {box2} to index {x}")
                groups[x] |= {box1, box2}
                found = True
                break
        if not found:
            # print(f"Adding {box1} and {box2} to new index {i}")
            groups[i] = {box1, box2}
            i += 1
        groups = clean_groups(groups)
        connections_made += 1
        # print(f"Incrementing connections to {connections_made}")
        if connections_made >= n_connections:
            print(f"Made {connections_made} connections so breaking out.")
            break

    new_groups = []

    return groups


def main(filename: str, n_connections: int = 10) -> None:
    filepath = Path(__file__).parent / filename

    with open(filepath) as f:
        data = f.read().splitlines()

    junction_boxes: map[Box] = get_junction_boxes(data)
    pairs: combinations[tuple[Box, Box]] = combinations(junction_boxes, 2)
    distances: dict[tuple[Box, Box], float] = {a: a[0] - a[1] for a in pairs}
    ordered = sorted(distances.items(), key=lambda item: item[1])
    groups = process_distances(ordered, n_connections)
    groups_sizes: list[int]
    print()
    group_sizes: list[int] = []
    for x, links in groups.items():
        print(f"Group {x} size = {len(links)}")
        group_sizes.append(len(links))

    total = 1
    for group_size in sorted(group_sizes, reverse=True)[:3]:
        total *= group_size

    print(f"Answer = {total}")


if __name__ == "__main__":
    filename: str = "example-input.txt"
    filename = "real-input.txt"
    main(filename, 1000)
