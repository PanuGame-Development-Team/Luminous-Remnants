import pygame
from lib import *
from init import imgresource,screensize
from settings import *
class _AUTOPLAY:
    dest = [0,0]
    moving = False
    tick = 0
    outset = [screensize[0]/2,screensize[1]/2]
class Mouse(pygame.sprite.Sprite):
    angle = 0
    rotating = False
    pos = [screensize[0]/2,screensize[1]/2]
    resource_id = None
    showing = False
    image = None
    alpha = 0
    dalpha = 0
    loc = [0,0]
    autoplay = _AUTOPLAY()
    def update(self,screen,mousepos):
        if not AUTOPLAY.ENABLE:
            self.pos = mousepos
        else:
            if self.autoplay.moving:
                self.pos = sectionformula(*self.autoplay.outset,*self.autoplay.dest,approaching(self.autoplay.tick,0,1,AUTOPLAY.MOUSE))
                self.autoplay.tick += 1
                if self.autoplay.tick > AUTOPLAY.MOUSE.TICK:
                    self.autoplay.tick = 0
                    self.autoplay.moving = False
            else:
                self.autoplay.outset = self.pos
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
        pygame.draw.lines(screen,MOUSE.COLOR,1,starposls(3,STAR.RADIUS,self.angle,*self.pos))
        pygame.draw.lines(screen,MOUSE.COLOR,1,starposls(3,STAR.RADIUS,60 + self.angle,*self.pos))
        pygame.draw.circle(screen,MOUSE.COLOR,self.pos,1,1)
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