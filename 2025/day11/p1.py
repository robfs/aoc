from dataclasses import dataclass
from pathlib import Path
from typing import Self


@dataclass
class Device:
    name: str
    outputs: set[str]

    @classmethod
    def from_row(cls, row: str) -> Self:
        name, output_string = row.split(":")
        outputs = set(output_string.strip().split())
        return cls(name, outputs)


def main(filename: str) -> None:
    filepath = Path(__file__).parent / filename

    with open(filepath) as f:
        data = f.read().splitlines()

    devices = list(map(Device.from_row, data))
    device_map = {device.name: device for device in devices}

    start: str = "you"
    stop: str = "out"
    you = device_map[start]
    paths: list[list[Device]] = [[you]]
    while not all([stop in path[-1].outputs for path in paths]) or not paths:
        new_paths: list[list[Device]] = []
        for path in paths:
            last_step = path[-1]
            if stop in last_step.outputs:
                new_paths.append(path)
                continue
            outputs = last_step.outputs
            connected_devices = [device_map[output] for output in outputs]
            for device in connected_devices:
                new_paths.append(path + [device])
        paths = new_paths
    print(f"{len(paths)} paths")


if __name__ == "__main__":
    filename: str = "example-input.txt"
    filename = "real-input.txt"

    main(filename)
