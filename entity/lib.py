from math import sqrt
from ca import *
from uuid import uuid4
from entity.settings import *
class Pos(DataStructure):
    def __init__(self,x:float,y:float,stx:int = 1536,sty:int = 864):
        self.x = x
        self.y = y
        self.stx = stx
        self.sty = sty
    def __add__(self,other):
        if self.stx != other.stx or self.sty != other.sty:
            raise ValueError("Can't add two pos with different standard. LHS:(%d,%d) RHS:(%d:%d)"%(self.stx,self.sty,other.stx,other.sty))
        if isinstance(other,type(self)):
            return Pos(self.x + other.x,self.y + other.y,self.stx,self.sty)
    def __truediv__(self,other):
        if type(other) in [int,float]:
            return Pos(self.x / other,self.y / other,self.stx,self.sty)
    def __sub__(self,other) -> float:
        if self.stx != other.stx or self.sty != other.sty:
            raise ValueError("Can't sub two pos with different standard. LHS:(%d,%d) RHS:(%d:%d)"%(self.stx,self.sty,other.stx,other.sty))
        if isinstance(other,type(self)):
            return (self.x - other.x) ** 2 + (self.y - other.y) ** 2
    def scale(self,newx:int,newy:int):
        self.x = self.x * newx / self.stx
        self.y = self.y * newy / self.sty
        self.stx = newx
        self.sty = newy
        return self
    def t(self,scalex=None,scaley=None) -> tuple:
        if scalex and scaley:
            self.scale(scalex,scaley)
        return self.x,self.y
    def d(self,other) -> float:
        return sqrt(self - other)
class Resource_id(DataStructure):
    def __init__(self,id:str):
        self.id = id
    def set_rman(self,rman) -> None:
        self.rman = rman
    def get(self):
        assert hasattr(self,"rman")
        return self.rman.mapper[self.id]
class ResourceManager:
    def __init__(self,randstr_function=lambda:uuid4().hex):
        self.mapper = {}
        self.rand = randstr_function
    def register(self,resource) -> Resource_id:
        rid = Resource_id(self.rand())
        while rid.id in self.mapper:
            rid = Resource_id(self.rand())
        self.mapper[rid.id] = resource
        rid.set_rman(self)
        return rid
def average(*args) -> Pos:
    p = Pos(0,0,args[0].stx,args[0].sty)
    for i in args:
        if DEBUG.POS_STANDARD:
            assert p.stx == i.stx
            assert p.sty == i.sty
        p = p + i
    return p / len(args)