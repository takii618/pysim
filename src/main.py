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
# print(connection1)
# print(connection2)

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
# print(connection1_1,connection2_1)
# lol iknow there is barely a difference we just used here the __getitem__ method
# object[smth] actually invokes object.__getitem__(smth) cool ha!

#-----------------------
# third the even less hard way, 
#-----------------------

# diagram2 = Diagram()
#
#
# const_block2 = Constant("const_block2", 3)
# gain_block2 = Gain("gain_block2",4.2)
# scope_block2 = Scope("scope_block2")
#
# diagram2.add_blocks(const_block2,gain_block2,scope_block2)
# connection1_2 = diagram2.connect(const_block2,gain_block2)
# connection2_2 = diagram2.connect(gain_block2,scope_block2)
# print(connection1_2,connection2_2)

# here its improved a bit more, now if the blocks has one input port or one output port you dont need to specify the port in connecting, you can just give connect() the blocks, or a block and a port


#-----------------------
# fourth the even even less hard way for evaluation, 
#-----------------------

diagram3 = Diagram()
cnst = Constant('cnst',8)
gain = Gain("gain",3)
sm = Summer("sm")
scp = Scope("scp")

diagram3.add_blocks(cnst,gain, sm, scp)
diagram3.connect(cnst, gain)
diagram3.connect(gain, sm["u0"])
diagram3.connect(cnst, sm["u1"])
diagram3.connect(sm, scp)

print(diagram3.connections)
print(diagram3.execution_order())
print(diagram3.evaluate())

#here we made the the topological sort for the graph to know which blocks to excute
#first so we can implement a general evaluate method for the whole diagram, but
#still, now our tiny primitive engine only supports static blocks and cycles or loops will get regected,...

