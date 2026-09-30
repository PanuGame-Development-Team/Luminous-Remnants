from ca import *
from entity.entity import Entity
class Controller(Interface):
    showing = False
    def __init__(self,pos:Entity.Pos):
        self.pos = pos
    def set_pos(self,pos:Entity.Pos) -> None:
        self.pos.x = pos.x
        self.pos.y = pos.y
        self.pos.stx = pos.stx
        self.pos.sty = pos.sty
    def get_pos(self) -> Entity.Pos:
        return self.pos.copy()
    def click(self) -> None:...
    def tick(self) -> None:...