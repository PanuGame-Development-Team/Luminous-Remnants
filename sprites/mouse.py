import pygame
from lib import *
class Mouse(pygame.sprite.Sprite):
    angle = 0
    rotating = False
    pos = [0,0]
    resource_id = None
    showing = True
    def update(self,screen,mousepos):
        self.pos = mousepos
        if self.rotating:
            self.angle += 3
            if self.angle >= 60:
                self.rotating = False
                self.angle = 0
        pygame.draw.lines(screen,[255,255,255],1,starposls(3,15,self.angle,*self.pos))
        pygame.draw.lines(screen,[255,255,255],1,starposls(3,15,60 + self.angle,*self.pos))
    def click(self):
        self.rotating = True
        # if self.resource_id:
        #     self.playing = True