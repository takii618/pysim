from __future__ import annotations
from enum import Enum
import numpy as np


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
    """class Diagram with two attributes a list of blocks and list of connections,
    you can add blocks with:
        diagram.add_block
        or diagram.add_blocks"""

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

    def connect(self, src: Port | Block, dest: Port | Block) -> Connection:
        """ method of the class Diagram, use it to connect ports, inputs -> outputs        or you can give it blocks if the connecting is non ambiguous, improvements
        needed"""

        if isinstance(src, Block):
            src = resolve_port(src, Direction.OUTPUT)
        if isinstance(dest, Block):
            dest = resolve_port(dest, Direction.INPUT)

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
    
    def execution_order(self):
        adjacency = {block: set() for block in self.blocks}
        indegree = {block: 0 for block in self.blocks}

        for c in self.connections:
            src = c.source.owner
            dst = c.destination.owner

            if dst not in adjacency[src]:
                adjacency[src].add(dst)
                indegree[dst] += 1

        queue = [
            block for block in self.blocks
            if indegree[block] == 0
        ]

        order = []

        while queue:
            block = queue.pop(0)
            order.append(block)

            for neighbor in adjacency[block]:
                indegree[neighbor] -= 1

                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        if len(order) != len(self.blocks):
            raise ValueError("Cycle detected in diagram")

        return order

    def evaluate(self):

        incoming = {
                c.destination : c
                for c in self.connections
                }
        values = {}
        results = {}

        for block in self.execution_order():

            inputs = {}

            for name, port in block.inputs.items():
                connection = incoming.get(port)

                if connection is None:
                    raise ValueError(
                        f"Unconnected input: {block.name}.{name}"
                    )

                inputs[name] = values[connection.source]

            outputs = block.evaluate(inputs)

            for name, value in outputs.items():
                values[block.outputs[name]] = value

            results[block.name] = outputs

        return results


def resolve_port(block : Block, direction : Direction):
    ports = block.inputs if direction == Direction.INPUT else block.outputs
    if len(ports) <1:
        raise ValueError(f"the block {block} has no {direction} ports")
    if len(ports) > 1:
        raise ValueError(f"the block {block} has multiple ({len(ports)}){direction} ports")
    return next(iter(ports.values()))
