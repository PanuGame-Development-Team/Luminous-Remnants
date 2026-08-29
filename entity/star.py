from ca import *
from entity.picture import Picture
from entity.lib import Pos
class Star(Interface):
    def __init__(self,direction:float,rotation:float,static_pos:Pos,locked:bool,picture:Picture|None=None):
        self.direction = direction
        self.rotation = rotation
        self.pos = static_pos
        self.locked = locked
        self.pic = picture
    def tick(self) -> None:...
    def click(self) -> None:...