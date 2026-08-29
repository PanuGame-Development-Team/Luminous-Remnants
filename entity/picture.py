from ca import *
from entity.lib import Resource_id
class Picture(Interface):
    def __init__(self,resource_id:Resource_id):
        self.showing = False
        self.resource_id = resource_id
        self.alpha = 0
        self.dalpha = 0
    def play(self) -> None:...
    def tick(self) -> None:...
    def stop(self) -> None:...