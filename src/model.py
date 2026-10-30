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

