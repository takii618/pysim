from model import *

diagram = Diagram()

gain1 = Gain("gain1",3)
gain2 = Gain("gain2",4)
scopy = Scope("scopy")

const = Constant("in", 8)
sum = Summer("boo",3)
diagram.add_blocks(gain1,gain2,scopy,const,sum)
diagram.connect(const["u"],gain1["y"])

print(diagram.connections)




