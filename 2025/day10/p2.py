from dataclasses import dataclass, field
from pathlib import Path
from pprint import pprint
from typing import Literal, Self

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


@dataclass
class Button:
    _schematic: str
    n_lights: int
    schematic: list[int] = field(default_factory=list)
    bit_list: list[Literal[0, 1]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.schematic = eval(self._schematic.replace("(", "[").replace(")", "]"))
        self.bit_list = [1 if i in self.schematic else 0 for i in range(self.n_lights)]


@dataclass
class Machine:
    available_buttons: list[Button]
    n_lights: int
    _joltage_string: str
    state: list[int] = field(default_factory=list)
    target: list[int] = field(default_factory=list)

    @property
    def joltage_string(self) -> str:
        return self._joltage_string.strip("{}")

    @property
    def target_joltage(self) -> list[int]:
        return list(map(int, self.joltage_string.split(",")))

    def __post_init__(self) -> None:
        self.target = self.target_joltage

    @classmethod
    def from_input(cls, input_row: str) -> Self:
        inputs = input_row.split()
        lights = inputs.pop(0)
        n_lights = len(lights.strip("[]"))
        joltage_input = inputs.pop(-1)
        buttons = [Button(input, n_lights) for input in inputs]
        return cls(buttons, n_lights, joltage_input)

    def push_button(self, button: Button, n: int = 1) -> None:
        for i in button.schematic:
            self.state[i] += n

    def matrix(self) -> np.ndarray:
        rows: list[list[int]] = []
        for i in range(self.n_lights):
            row = [button.bit_list[i] for button in self.available_buttons]
            rows.append(row)

        return np.array(rows)

    def target_array(self) -> np.ndarray:
        return np.array(self.target)  # .reshape((-1, 1))

    def solve(self) -> int | None:
        A = self.matrix()
        b = self.target_array()
        n_buttons = len(self.available_buttons)

        c = np.ones(n_buttons)
        constraints = LinearConstraint(A, b, b)
        bounds = Bounds(0, np.inf)
        integrality = np.ones(n_buttons)
        result = milp(
            c=c, constraints=constraints, bounds=bounds, integrality=integrality
        )

        if result.success:
            total_presses = int(np.sum(result.x))
            print(f"Solution found: {total_presses} total presses")
            print(f"Button presses: {[int(x) for x in result.x]}")
            # Verify the solution
            achieved = A @ result.x
            print(f"Target:   {b}")
            print(f"Achieved: {[int(x) for x in achieved]}")
            return total_presses
        else:
            print(f"No solution found. Status: {result.message}")
            return None


def main(filename: str) -> None:
    filepath = Path(__file__).parent / filename
    with open(filepath) as f:
        data: list[str] = f.read().splitlines()

    machines = list(map(Machine.from_input, data))

    total: int = 0
    for i, machine in enumerate(machines):
        print(f"\nMachine {i + 1}")

        result = machine.solve()
        if result is not None:
            total += result
        else:
            print("Failed to solve this machine!")

    print(f"\nTotal: {total}")


if __name__ == "__main__":
    filename: str = "example-input.txt"
    filename = "real-input.txt"

    main(filename)
