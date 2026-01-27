import pygame
from lib import *
from random import randint,choice
from settings import *
class Star(pygame.sprite.Sprite):
    hovertick = 0
    hovering = False
    rmax = STAR.RADIUS
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
                color = color_adapt(STAR.LOCKED_COLOR,GENERAL.BG_COLOR,alpha,STAR.SHOW_FACTOR,0)
                pygame.draw.aalines(screen,color,1,starposls(5,STAR.RADIUS,0,*self.pos))
            else:
                color = color_adapt(STAR.COLOR,GENERAL.BG_COLOR,alpha,STAR.SHOW_FACTOR,0)
                dist = calc_distance_sq(*self.pos,*mouse.pos) 
                if dist <= 225 and not self.hovering:
                    self.hovering = True
                    self.rmax = STAR.RADIUS
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
                if self.r != STAR.RADIUS:
                    pygame.draw.aalines(screen,color,1,starposls(5,STAR.RADIUS - self.r,self.angle,*self.pos))
                if self.r != 0:
                    pygame.draw.circle(screen,color,self.pos,self.r,1)
                    pygame.draw.circle(screen,color,self.pos,self.r * STAR.RADIUS_FACTOR,1)
    def hoverR(self):
        if self.hovering:
            if self.hovertick < STAR.HOVER.TICK:
                self.hovertick += 1
                return approaching(self.hovertick,self.rmin,self.rmax,STAR.HOVER) + self.rmin
            return self.rmax
        else:
            if self.hovertick < STAR.HOVER.TICK:
                self.hovertick += 1
                return self.rmax - approaching(self.hovertick,self.rmin,self.rmax,STAR.HOVER)
            return self.rmin