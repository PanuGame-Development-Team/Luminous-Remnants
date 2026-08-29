from entity.entity import Entity
from usecase.variables import var
from usecase.settings import PICTURE
class Picture(Entity.Picture):
    def stop(self) -> None:
        if self.showing:
            self.dalpha = -PICTURE.ALPHA_DECAY
    def play(self) -> None:
        self.showing = True
        self.dalpha = PICTURE.ALPHA_DECAY
    def tick(self):
        self.alpha += self.dalpha
        if self.alpha >= PICTURE.MAX_ALPHA:
            self.alpha = PICTURE.MAX_ALPHA
            self.dalpha = 0
        elif self.alpha <= 0:
            self.alpha = 0
            self.dalpha = 0
            self.showing = False
        if self.showing:
            var.alpha = self.alpha