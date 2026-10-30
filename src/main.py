from model import *
from blocks import *

# creating simple diagram const -> gain -> scope

#-----------------------
# first the hard way, 
#-----------------------

diagram = Diagram()
const_block = Constant("const_block", 1)
gain_block = Gain("gain_block",3.1)
scope_block = Scope("scope_block")

diagram.add_blocks(const_block,gain_block,scope_block)

# const_block.outputs["y"] return the port with direction output named y
# for now all output ports are called y (if there is only one output)
# the same goes for inputs (if there are many inputs, then there names would be u1,u2 ,...)
connection1 = diagram.connect(const_block.outputs["y"],gain_block.inputs["u"])
connection2 = diagram.connect(gain_block.outputs["y"],scope_block.inputs["u"])
print(connection1)
print(connection2)

#-----------------------
# second the less hard way, 
#-----------------------

diagram1 = Diagram()


const_block1 = Constant("const_block1", 2)
gain_block1 = Gain("gain_block1",4.1)
scope_block1 = Scope("scope_block1")

diagram1.add_blocks(const_block1,gain_block1,scope_block1)
connection1_1 = diagram1.connect(const_block1["y"],gain_block1["u"])
connection2_1 = diagram1.connect(gain_block1["y"],scope_block1["u"])
print(connection1_1,connection2_1)
# lol iknow there is barely a difference we just used here the __getitem__ method
# object[smth] actually invokes object.__getitem__(smth) cool ha!
