from __future__ import annotations
from model import *


class Gain(Block):

    def __init__(self, name: str, k: float):
        super().__init__(name)
        self.k = k
        self.add_input("u")
        self.add_output("y")

    def evaluate(self, u: float) -> float:
        return self.k * u

    def __repr__(self) -> str:
        return f"Gain(name={self.name!r}, k={self.k})"


class Constant(Block):
    def __init__(self, name: str, value: float):
        super().__init__(name)
        self.value = value
        self.add_output("y")

    def evaluate(self) -> float:
        return self.value

    def __repr__(self) -> str:
        return f"Constant(name={self.name!r}, value={self.value})"

class Summer(Block):
    def __init__(self, name: str, n_inputs: int = 2):
        super().__init__(name)
        if n_inputs < 1:
            raise ValueError("Summer needs at least one input")
        self.n_inputs = n_inputs

        for i in range(n_inputs):
            self.add_input(f"u{i}")
            self.add_output("y")

    def evaluate(self, *inputs: float) -> float:

        if len(inputs) != self.n_inputs:
            raise ValueError("Incorrect number of inputs")
        return sum(inputs)

    def __repr__(self) -> str:
        return f"Summer(name={self.name!r}, n_inputs={self.n_inputs})"

class Scope(Block):
    def __init__(self, name: str):
        super().__init__(name)

        self.add_input("u")
        self.time: list[float] = []
        self.values: list[float] = []

    def record(self, t:float, u:float) -> None:
        self.time.append(t)
        self.values.append(u)

    def clear(self) -> None:
        self.time.clear()
        self.values.clear()

    def __repr__(self) -> str:
        return f"Scope(name={self.name!r}, samples={len(self.time)})"

