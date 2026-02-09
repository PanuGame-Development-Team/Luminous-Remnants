import pygame
from lib import *
from settings import *
from random import randint,choice,random
class Meteor(pygame.sprite.Sprite):
    def __init__(self,fromx,fromy,destx,desty,*groups):
        super().__init__(*groups)
        self.outset = [fromx,fromy]
        self.dest = [destx,desty]
        self.tick = 0
        self.angle = randint(0,359)
        self.rotation = choice([-1,1]) * METEOR.ROTATION
    def update(self,screen,speed,alpha):
        self.angle += self.rotation
        self.angle %= 360
        self.outset[0] += speed
        self.dest[0] += speed
        if self.tick >= METEOR.STAY_TICK:
            start = self.dest
        else:
            start = sectionformula(*self.outset,*self.dest,scrolling(self.tick,METEOR.STAY_TICK,1))
        if self.tick <= METEOR.SLIDE_TICK:
            end = self.outset
        else:
            end = sectionformula(*self.outset,*self.dest,scrolling(self.tick - METEOR.SLIDE_TICK,METEOR.STAY_TICK,1))
        color = color_adapt(STAR.COLOR,GENERAL.BG_COLOR,alpha,STAR.SHOW_FACTOR,0)
        if calc_distance_sq(*start,*end) > (METEOR.FRONT_COVER_RADIUS + METEOR.BACK_COVER_RADIUS) ** 2:
            linestart = circle_border(METEOR.FRONT_COVER_RADIUS,*start,*end)
            lineend = circle_border(METEOR.BACK_COVER_RADIUS,*end,*start)
            pygame.draw.aaline(screen,color,linestart,lineend)
        pygame.draw.aalines(screen,color,1,starposls(5,METEOR.FRONT_STAR_RADIUS,self.angle,*start))
        pygame.draw.aalines(screen,color,1,starposls(5,METEOR.BACK_STAR_RADIUS,self.angle,*end))
        self.tick += 1
        if self.tick > METEOR.STAY_TICK + METEOR.SLIDE_TICK:
            self.kill()
class MeteorRainHandler:
    def handle(self,group,tick):
        ...