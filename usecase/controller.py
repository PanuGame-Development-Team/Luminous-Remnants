from ca import *
from entity.entity import Entity
from usecase.galaxy import Galaxy
class Controller(Interface):
    showing = False
    def __init__(self,pos:Entity.Pos):
        self.pos = pos
    def set_pos(self,pos:Entity.Pos) -> None:
        self.pos = pos
    def get_pos(self) -> Entity.Pos:
        return self.pos
    def click(self) -> None:...
    def tick(self) -> None:...