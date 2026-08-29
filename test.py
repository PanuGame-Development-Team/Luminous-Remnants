from os import listdir
from importlib import import_module
ls = listdir("tests")
for i in ls:
    if i.endswith(".py"):
        filename = i.removesuffix(".py")
        testmodname = "tests." + filename
        try:
            mod = import_module(testmodname)
            if hasattr(mod,"status"):
                if mod.status == "OK":
                    print("[ OK ] - [%-20s]: Passed." % filename)
                if mod.status == "WARN":
                    print("[WARN] - [%-20s]: %s" % (filename,mod.warn))
            else:
                print("[DEBG] - [%-20s]: No status found." % filename)
        except Exception as e:
            print("[ERR ] - [%-20s]: Test failed." % filename)
            raise e
