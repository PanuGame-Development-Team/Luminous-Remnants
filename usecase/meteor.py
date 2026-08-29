from entity.entity import Entity
from usecase.settings import METEOR
class Meteor(Entity.Meteor):
    living_tick = 0
    def __init__(self,container:list,*args):
        super().__init__(*args)
        self.container = container
    def tick(self) -> None:
        self.living_tick += 1
        self.direction += self.rotation
        if self.living_tick > METEOR.STAY_TICK + METEOR.SLIDE_TICK:
            self.container.remove(self)