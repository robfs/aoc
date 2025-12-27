from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from pprint import pprint
from typing import Self


@dataclass
class Button:
    _schematic: str
    n_lights: int
    bin_string: str = ""
    integer: int = 0

    def __post_init__(self) -> None:
        self.schematic = eval(self._schematic.replace("(", "[").replace(")", "]"))
        bin_string = ""
        for i in range(self.n_lights):
            bin_string += "1" if i in self.schematic else "0"
        self.bin_string = bin_string
        self.integer = int(self.bin_string, 2)


@dataclass(frozen=True)
class Joltage:
    _requirements: str


@dataclass
class Machine:
    n_lights: int
    _target_string: str
    available_buttons: list[Button]
    joltage_required: Joltage
    _state: int = 0
    target: int = 0

    @property
    def target_string(self) -> str:
        return self._target_string.strip("[]").replace(".", "0").replace("#", "1")

    def __post_init__(self) -> None:
        self.target = int(self.target_string, 2)

    def reset(self) -> None:
        self._state = 0

    @classmethod
    def from_input(cls, input_row: str) -> Self:
        inputs = input_row.split()
        panel_input = inputs.pop(0)
        n_lights = len(panel_input) - 2
        joltage_input = inputs.pop(-1)

        joltage = Joltage(joltage_input)
        buttons = [Button(input, n_lights) for input in inputs]

        return cls(n_lights, panel_input, buttons, joltage)

    def push_button(self, button: Button) -> None:
        self._state ^= button.integer

    @property
    def state(self) -> str:
        return f"{bin(self._state)[2:]:0>{self.n_lights}}"

    @property
    def target_state(self) -> str:
        return f"{bin(self.target)[2:]:0>{self.n_lights}}"

    def solve(self) -> int:
        i = 0
        while self._state - self.target != 0:
            i += 1
            # print(f"Trying to achieve {self.target_state} using {i} buttons")
            combos = combinations(self.available_buttons, i)
            for combo in combos:
                self.reset()
                for button in combo:
                    self.push_button(button)
                if self._state == self.target:
                    break
        # print(f"SUCCESS: {combo} yields {self.target_state}")
        return i


def main(filename: str) -> None:
    filepath = Path(__file__).parent / filename
    with open(filepath) as f:
        data: list[str] = f.read().splitlines()

    machines = list(map(Machine.from_input, data))
    total: int = 0
    for machine in machines:
        total += machine.solve()

    print(f"Solution: {total}")


if __name__ == "__main__":
    filename: str = "example-input.txt"
    filename = "real-input.txt"

    main(filename)
