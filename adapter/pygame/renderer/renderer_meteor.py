from usecase.usecase import UseCase
from adapter.settings import *
from adapter.pygame.renderer.uimath import *
from random import random,choice
import pygame
class MeteorRenderer(UseCase.Renderer):
    def __init__(self,display:pygame.surface.Surface,scrsize):
        self.display = display
        self.scrsize = scrsize
    def render(self,object:UseCase.Meteor):
        dx = abs(object.fpos.x - object.tpos.x)
        left = (min(object.fpos.x,object.tpos.x) + UseCase.var.scroffset) % (GENERAL.GRAPH_WIDTH * self.scrsize[0])
        right = dx + left
        marginx = max(METEOR.FRONT_COVER_RADIUS,METEOR.BACK_COVER_RADIUS)
        if left > self.scrsize[0] + marginx:
            right -= GENERAL.GRAPH_WIDTH * self.scrsize[0]
        if right < -marginx:
            return
        fpos = list(object.fpos.t())
        tpos = list(object.tpos.t())
        if fpos[0] < tpos[0]:
            fpos[0] = right - dx
            tpos[0] = right
        else:
            fpos[0] = right
            tpos[0] = right - dx
        if object.living_tick >= METEOR.STAY_TICK:
            start = tpos
        else:
            start = section_formula(*fpos,*tpos,sine_slide(object.living_tick,METEOR.STAY_TICK,1))
        if object.living_tick <= METEOR.SLIDE_TICK:
            end = fpos
        else:
            end = section_formula(*fpos,*tpos,sine_slide(object.living_tick - METEOR.SLIDE_TICK,METEOR.STAY_TICK,1))
        color = color_adapt(METEOR.COLOR,GENERAL.BG_COLOR,UseCase.var.alpha,METEOR.SHOW_FACTOR,0)
        if UseCase.Entity.Pos(*start) - UseCase.Entity.Pos(*end) > (METEOR.FRONT_COVER_RADIUS + METEOR.BACK_COVER_RADIUS) ** 2:
            linestart = circle_border(METEOR.FRONT_COVER_RADIUS,*start,*end)
            lineend = circle_border(METEOR.BACK_COVER_RADIUS,*end,*start)
            pygame.draw.aaline(self.display,color,linestart,lineend)
        pygame.draw.aalines(self.display,color,1,starposls(5,METEOR.FRONT_STAR_RADIUS,object.direction,*start))
        pygame.draw.aalines(self.display,color,1,starposls(5,METEOR.BACK_STAR_RADIUS,-object.direction,*end))
class MeteorRainProcesser:
    def __init__(self,screensize):
        self.raining = False
        self.rain_tick = 0
        self.angle = None
        self.lr = None
        self.tick = 0
        self.count = []
        self.total = 0
        self.screensize = screensize
    def handle(self,group:list):
        if not METEOR.ENABLE:
            return
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
        if self.tick > METEOR.RAIN.SPACING_TICK:
            self.total -= self.count.pop(0)
            if self.total < METEOR.RAIN.METEOR_LIMIT:
                self.angle = randlr(METEOR.MIN_DIRECTION,METEOR.MAX_DIRECTION) / 180 * math.pi
                self.lr = choice([-1,1])
                self.raining = True
                self.rain_tick = 0
                self.total = METEOR.RAIN.SPACING_TICK
                self.count = [1 for i in range(METEOR.RAIN.STAY_TICK)]
    def handle_rain(self,group:list):
        if self.rain_tick < METEOR.RAIN.DURATION:
            if self.rain_tick % METEOR.RAIN.TICK_PER_MET == 0:
                self.drop(group,self.angle,self.lr)
            self.rain_tick += 1
        else:
            self.raining = False
    def drop(self,group:list,angle=None,lr=None):
        fromx = randlr(-self.screensize[0],self.screensize[0] * 2)
        fromy = randlr(0,self.screensize[1] * METEOR.FROMY_FACTOR)
        length = randlr(METEOR.MIN_LENGTH,METEOR.MAX_LENGTH)
        if not angle:
            angle = randlr(METEOR.MIN_DIRECTION,METEOR.MAX_DIRECTION) / 180 * math.pi
        if not lr:
            lr = choice([-1,1])
        tox = fromx + lr * length * math.cos(angle)
        toy = fromy + length * math.sin(angle)
        group.append(UseCase.Meteor(group,UseCase.Entity.Pos(fromx,fromy,*self.screensize),UseCase.Entity.Pos(tox,toy,*self.screensize),choice([1,-1]),random() * 360))