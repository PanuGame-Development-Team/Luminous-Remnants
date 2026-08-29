from entity.lib import ResourceManager
from uuid import uuid4
from time import time
rman = ResourceManager(uuid4)
n = rman.register("12344321")
t = rman.register(12344321)
assert n.get() == "12344321"
assert t.get() == 12344321
t0 = time()
for i in range(1000000):
    rman.register(time())
t1 = time()
if t1 - t0 <= 10:
    status = "OK"
else:
    status = "WARN"
    warn = "The program may have performance problems.Expected 1.0e+05reg/s,Measured %.5ereg/s"%(1e6/(t1-t0))