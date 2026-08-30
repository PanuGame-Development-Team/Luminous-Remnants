from usecase.usecase import UseCase
from adapter.settings import *
from adapter.pygame.renderer.uimath import *
import pygame
class StarRenderer(UseCase.Renderer):
    def __init__(self,display:pygame.surface.Surface,scrsize):
        self.display = display
        self.scrsize = scrsize
    def render(self,object:UseCase.Star):
        center = list(object.pos.t())
        center[0] = (center[0] + UseCase.var.scroffset) % (GENERAL.GRAPH_WIDTH * self.scrsize[0])
        if center[0] > self.scrsize[0] + STAR.RADIUS:
            center[0] -= GENERAL.GRAPH_WIDTH * self.scrsize[0]
        if center[0] < 0 - STAR.RADIUS:
            return
        if object.locked:
            color = color_adapt(STAR.LOCKED_COLOR,GENERAL.BG_COLOR,UseCase.var.alpha,STAR.SHOW_FACTOR,0)
            pygame.draw.aalines(self.display,color,1,starposls(5,STAR.RADIUS,0,*center))
        else:
            color = color_adapt(STAR.COLOR,GENERAL.BG_COLOR,UseCase.var.alpha,STAR.SHOW_FACTOR,0)
            object.r = r = self.hoverR(object)
            if r != STAR.RADIUS:
                pygame.draw.aalines(self.display,color,1,starposls(5,STAR.RADIUS - r,object.direction,*center))
            if r != 0:
                pygame.draw.circle(self.display,color,center,r,1)
                pygame.draw.circle(self.display,color,center,r * STAR.RADIUS_FACTOR,1)
    def hoverR(self,object:UseCase.Star):
        if object.hovering:
            if object.hovertick < STAR.HOVER_TICK:
                object.hovertick += 1
                return approaching(object.hovertick,STAR.HOVER_TICK,object.rmin,object.rmax) + object.rmin
            return object.rmax
        else:
            if object.hovertick < STAR.HOVER_TICK:
                object.hovertick += 1
                return object.rmax - approaching(object.hovertick,STAR.HOVER_TICK,object.rmin,object.rmax)
            return object.rmin