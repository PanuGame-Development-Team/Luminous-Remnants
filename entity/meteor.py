from ca import *
from entity.lib import Pos
class Meteor(Interface):
    def __init__(self,fpos:Pos,tpos:Pos,rotation:float,direction:float):
        self.fpos = fpos
        self.tpos = tpos
        self.rotation = rotation
        self.direction = direction
    def tick(self) -> None:...