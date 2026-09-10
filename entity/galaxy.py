from ca import *
from entity.star import Star
from entity.lib import Pos,average
from settings import STAR
class Galaxy(Interface):
    def __init__(self,name:str,label:str,stars:list[Star],lines:list[list[Pos]]):
        self.label = label
        self.name = name
        self.stars = stars
        self.center = average(*[star.pos for star in stars])
        self.r = sum(map(lambda star:star.pos.d(self.center),stars)) / len(stars)
        self.lines = lines
        self.left = min([star.pos.x for star in stars]) - STAR.RADIUS
        self.right = max([star.pos.x for star in stars]) + STAR.RADIUS
    def tick(self) -> None:...