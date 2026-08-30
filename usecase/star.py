from entity.entity import Entity
from usecase.settings import *
class Star(Entity.Star):
    hovering = False
    hovertick = 0
    rmin = 0
    rmax = 0
    r = 0
    def tick(self) -> None:
        self.direction += self.rotation
        if self.direction >= 360:
            self.direction -= 360
        elif self.direction < 0:
            self.direction += 360
        if self.hovertick < STAR.HOVER_TICK:
            self.hovertick += 1
        if not self.locked:
            self.pic.tick()
    def hover(self) -> None:
        self.hovering = True
        self.hovertick = 0
        self.rmax = STAR.RADIUS
        self.rmin = self.r
    def dehover(self) -> None:
        self.hovering = False
        self.hovertick = 0
        self.rmin = 0
        self.rmax = self.r