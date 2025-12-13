from pathlib import Path


class Dial:
    def __init__(self, value: int = 0, max: int = 99):
        self.value: int = value
        self.max: int = max
        self.turned_through_zero: int = 0

    def turn(self, instruction: str) -> int:
        start = self.value
        direction = instruction[0]
        amount = int(instruction[1:])
        if direction == "L":
            amount *= -1
        divisor = self.max + 1
        unadjusted_value = self.value + amount
        n_turns, new_value = divmod(unadjusted_value, divisor)
        if direction == "L":
            n_turns *= -1
            if start == 0:
                n_turns -= 1
            if new_value == 0:
                n_turns += 1
        self.turned_through_zero += abs(n_turns)
        self.value = new_value
        return self.value


def main(filename: str) -> None:
    path = Path(__file__).parent / filename
    with open(path) as f:
        data = f.read().splitlines()
    dial = Dial(50)
    total = 0
    x = 0
    for instruction in data:
        start = dial.value
        through_zero = dial.turned_through_zero
        value = dial.turn(instruction)
        through_zero -= dial.turned_through_zero
        print(f"{start=} + {instruction=} -> {value=} ({abs(through_zero)})")
        if value == 0:
            total += 1
        if x > 0:
            x -= 1
            continue
        n = input("N times: ")
        if n.isdigit():
            x = int(n) - 1
    print(f"Total times dial faced 0: {total}")
    print(f"Total times dial passed through 0: {dial.turned_through_zero}")
    return None


if __name__ == "__main__":
    filename = "example-input.txt"
    filename = "real-input.txt"
    main(filename)
