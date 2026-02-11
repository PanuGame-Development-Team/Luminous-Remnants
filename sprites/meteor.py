import pygame
from lib import *
from settings import *
from random import randint,choice,random
from init import screensize
from math import cos,sin,pi
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
        color = color_adapt(METEOR.COLOR,GENERAL.BG_COLOR,alpha,METEOR.SHOW_FACTOR,0)
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
    raining = False
    rain_tick = 0
    angle = None
    lr = None
    tick = 0
    count = []
    total = 0
    def handle(self,group):
        self.tick += 1
        if self.raining:
            self.handle_rain(group)
            return
        probability = period_secion(self.tick,METEOR.RAIN.MAX_PROBABILITY,METEOR.RAIN.MIN_PROBABILITY,METEOR.RAIN.PROBABILITY_PERIOD)
        if probability > random():
            self.count.append(1)
            self.total += 1
            self.drop(group)
        else:
            self.count.append(0)
        if self.tick > METEOR.RAIN.STAY_TICK:
            self.total -= self.count.pop(0)
            if self.total < METEOR.RAIN.METEOR_LIMIT:
                self.angle = randlr(*METEOR.ANGLE) / 180 * pi
                self.lr = choice([-1,1])
                self.raining = True
                self.rain_tick = 0
                self.total = METEOR.RAIN.STAY_TICK
                self.count = [1 for i in range(METEOR.RAIN.STAY_TICK)]
    def handle_rain(self,group):
        if self.rain_tick < METEOR.RAIN.DURATION:
            if self.rain_tick % METEOR.RAIN.TICK_PER_MET == 0:
                self.drop(group,self.angle,self.lr)
            self.rain_tick += 1
        else:
            self.raining = False
    def drop(self,group,angle=None,lr=None):
        fromx = randlr(-screensize[0],screensize[0] * 2)
        fromy = randlr(0,screensize[1] * METEOR.FROMY_FACTOR)
        length = randlr(*METEOR.LENGTH)
        if not angle:
            angle = randlr(*METEOR.ANGLE) / 180 * pi
        if not lr:
            lr = choice([-1,1])
        destx = fromx + lr * length * cos(angle)
        desty = fromy + length * sin(angle)
        group.add(Meteor(fromx,fromy,destx,desty))