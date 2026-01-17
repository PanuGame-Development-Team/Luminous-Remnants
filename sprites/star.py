import pygame
from lib import *
from random import randint,choice
from settings import *
class Star(pygame.sprite.Sprite):
    hovertick = 0
    hovering = False
    rmax = 15
    rmin = 0
    r = 0
    def __init__(self,resource_id,pos,screensize,locked,*groups):
        super().__init__(*groups)
        self.resource_id = resource_id
        self.pos = pos
        self.angle = randint(0,359) if not locked else 0
        self.rotation = choice([-1,1]) if not locked else 0
        self.screensize = screensize
        self.locked = locked
    def update(self,screen,speed,alpha,in_screen,mouse):
        self.angle += self.rotation
        self.angle %= 360
        self.pos[0] += speed
        if self.pos[0] > self.screensize[0]:
            self.pos[0] -= self.screensize[0] * 2
        elif self.pos[0] < 0:
            self.pos[0] += self.screensize[0] * 2
        if in_screen:
            if self.locked:
                pygame.draw.aalines(screen,[128,128,128],1,starposls(5,15,0,*self.pos))
            else:
                color = color_adapt(LINE_COLOR,BG_COLOR,alpha,LINE_SHOW_FACTOR,0)
                dist = calc_distance_sq(*self.pos,*mouse.pos) 
                if dist <= 225 and not self.hovering:
                    self.hovering = True
                    self.rmax = 15
                    self.rmin = self.r
                    self.hovertick = 0
                    mouse.resource_id = self.resource_id
                elif dist > 225 and self.hovering:
                    self.hovering = False
                    self.rmin = 0
                    self.rmax =  self.r
                    self.hovertick = 0
                    if mouse.resource_id == self.resource_id:
                        mouse.resource_id = None
                self.r = self.hoverR()
                if self.r != 15:
                    pygame.draw.aalines(screen,color,1,starposls(5,15 - self.r,self.angle,*self.pos))
                if self.r != 0:
                    pygame.draw.circle(screen,color,self.pos,self.r,1)
                    pygame.draw.circle(screen,color,self.pos,self.r * 1.2,1)
    def hoverR(self):
        if self.hovering:
            if self.hovertick < 30:
                self.hovertick += 1
                return (1 - 1 / (0.2 * self.hovertick + 1)) / 0.85714 * (self.rmax - self.rmin) + self.rmin
            return self.rmax
        else:
            if self.hovertick < 30:
                self.hovertick += 1
                return self.rmax - (1 - 1 / (0.2 * self.hovertick + 1)) / 0.85714 * (self.rmax - self.rmin)
            return self.rmin