from pathlib import Path


class Dial:
    def __init__(self, value: int = 0, max: int = 99):
        self.value: int = value
        self.max: int = max

    def turn(self, instruction: str) -> int:
        direction = instruction[0]
        amount = int(instruction[1:])
        if direction == "L":
            amount *= -1
        self.value = (self.value + amount) % (self.max + 1)
        return self.value


def main(filename: str) -> None:
    path = Path(__file__).parent / filename
    with open(path) as f:
        data = f.read().splitlines()
    dial = Dial(50)
    total = 0
    for instruction in data:
        start = dial.value
        value = dial.turn(instruction)
        print(f"Dial turned from {start} to {value} using instruction {instruction}")
        if value == 0:
            total += 1
    print(f"Total times dial faced 0: {total}")
    return None


if __name__ == "__main__":
    filename = "example-input.txt"
    filename = "real-input.txt"
    main(filename)
