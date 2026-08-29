from usecase.usecase import UseCase
from adapter.controller import Controller
from adapter.settings import *
from adapter.pygame.renderer.uimath import *
from adapter.pygame.renderer.renderer_picture import PictureRenderer
import pygame
class ControllerRenderer(UseCase.Renderer):
    def __init__(self,display:pygame.surface.Surface,scrsize,pr:PictureRenderer):
        self.display = display
        self.scrsize = scrsize
        self.pr = pr
    def render(self,object:Controller):
        if object.hover_star and not object.hover_star.locked:
            self.pr.render(object.hover_star.pic)
        center = list(object.pos.t())
        center[0] = (center[0] + UseCase.var.scroffset) % (GENERAL.GRAPH_WIDTH * self.scrsize[0])
        direction = 60 * object.rotate_tick / CONTROLLER.ROTATE_TICK
        pygame.draw.lines(self.display,CONTROLLER.COLOR,1,starposls(3,STAR.RADIUS,direction,*center))
        pygame.draw.lines(self.display,CONTROLLER.COLOR,1,starposls(3,STAR.RADIUS,60 + direction,*center))
        pygame.draw.circle(self.display,CONTROLLER.COLOR,center,1,1)