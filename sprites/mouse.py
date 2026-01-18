import pygame
from lib import *
from init import imgresource,screensize
class Mouse(pygame.sprite.Sprite):
    angle = 0
    rotating = False
    pos = [0,0]
    resource_id = None
    showing = False
    image = None
    alpha = 0
    dalpha = 0
    loc = [0,0]
    def update(self,screen,mousepos):
        self.pos = mousepos
        if self.rotating:
            self.angle += 3
            if self.angle >= 60:
                self.rotating = False
                self.angle = 0
        if self.showing:
            self.alpha += self.dalpha
            if self.alpha >= 255:
                self.dalpha = 0
                self.alpha = 255
            elif self.alpha <= 0:
                self.dalpha = 0
                self.alpha = 0
                self.showing = False
            self.image.set_alpha(self.alpha)
            screen.blit(self.image,self.loc)
        pygame.draw.lines(screen,[255,255,255],1,starposls(3,15,self.angle,*self.pos))
        pygame.draw.lines(screen,[255,255,255],1,starposls(3,15,60 + self.angle,*self.pos))
        pygame.draw.circle(screen,[255,255,255],self.pos,1,1)
    def click(self):
        self.rotating = True
        if not self.showing and self.resource_id:
            self.showing = True
            self.image = imgresource[self.resource_id]
            self.loc = [0,0]
            self.loc[0] = abs(screensize[0] - self.image.get_size()[0]) / 2
            self.loc[1] = abs(screensize[1] - self.image.get_size()[1]) / 2
            self.dalpha = 3
        elif self.showing:
            self.dalpha = -3