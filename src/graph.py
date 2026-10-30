from __future__ import annotations
from enum import Enum

class Direction(Enum):
    INPUT = "input"
    OUTPUT = "output"


class Port:
    def __init__(self,name : str, direction : Direction, owner : Block):
        self.name = name
        self.direction = direction
        self.owner = owner

    def __repr__(self) -> str:
        return f"Port({self.owner.name}.{self.name}, {self.direction.name})"


class Block:

    def __init__(self, name: str):
        self.name = name
        self.inputs: dict[str, Port] = {}
        self.outputs: dict[str, Port] = {}
    
    def add_input(self, name: str) -> Port:
        if name in self.inputs:
            raise ValueError(f"Input '{name}'already exists, you forgot!!")

        port = Port(name, Direction.INPUT,self)
        self.inputs[name] = port
        return port


    def add_output(self, name: str) -> Port:
        if name in self.outputs:
            raise ValueError(f"output '{name}'already exists, you forgot!!")

        port = Port(name, Direction.OUTPUT,self)
        self.outputs[name] = port
        return port

    def __getitem__(self, name: str) -> Port:
        if name in self.inputs:
            return self.inputs[name]
        if name in self.outputs:
            return self.outputs[name]
        raise KeyError(f"Port '{name}' does not exist")

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name!r})"

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


class Connection:
    def __init__(self, src : Port, dest : Port):
        self.source = src
        self.destination = dest

    def __repr__(self) -> str:
        return (
               f"{self.source.owner.name}.{self.source.name}"
               f" -> "
               f"{self.destination.owner.name}.{self.destination.name}"
        )

class Diagram:
    def __init__(self):
        self.blocks = []
        self.connections = []

    def add_block(self, block: Block) -> Block:
        if block in self.blocks:
            raise ValueError(f"block {block.name} already in the diagram")
        self.blocks.append(block)
        return block

    def add_blocks(self, *blocks: Block) -> None:
        for block in blocks:
            self.add_block(block)

    def connect(self, src: Port, dest: Port) -> Connection:

        if src.owner not in self.blocks:
            raise ValueError("Source block not in diagram")

        if dest.owner not in self.blocks:
            raise ValueError("Destination block not in diagram")

        if src.direction != Direction.OUTPUT:
            raise ValueError("Source must be an output")

        if dest.direction != Direction.INPUT:
            raise ValueError("Destination must be an input")

        if src.owner.outputs.get(src.name) is not src:
            raise ValueError("Source port is not registered")

        if dest.owner.inputs.get(dest.name) is not dest:
            raise ValueError("Destination port is not registered")

        if any(c.destination is dest for c in self.connections):
            raise ValueError("Destination already connected")

        connection = Connection(src, dest)
        self.connections.append(connection)
        return connection

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

