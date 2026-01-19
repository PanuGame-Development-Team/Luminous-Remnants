import pygame
class Meteor(pygame.sprite.Sprite):
    def __init__(self,fromx,fromy,destx,desty,*groups):
        super().__init__(*groups)
        self.fromx = fromx
        self.fromy = fromy
        self.destx = destx
        self.desty = desty