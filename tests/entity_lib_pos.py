from entity.lib import Pos,average
a = Pos(1,2)
b = Pos(3,4)
c = Pos(5,6)
d = average(a,b,c)
assert d.x == 3.0
assert d.y == 4.0
status = "OK"