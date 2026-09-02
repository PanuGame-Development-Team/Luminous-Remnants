from usecase.usecase import UseCase
from adapter.settings import *
from adapter.pygame.renderer.uimath import *
from adapter.pygame.renderer.renderer_star import StarRenderer
import pygame
class GalaxyRenderer(UseCase.Renderer):
    def __init__(self,display:pygame.surface.Surface,scrsize,controller:UseCase.Controller,namefont:UseCase.Entity.Resource_id,labelfont:UseCase.Entity.Resource_id,sr:StarRenderer):
        self.display = display
        self.scrsize = scrsize
        self.controller = controller
        self.namefont = namefont
        self.labelfont = labelfont
        self.sr = sr
    def render(self,object:UseCase.Galaxy):
        left = (object.left + UseCase.var.scroffset) % (GENERAL.GRAPH_WIDTH * self.scrsize[0])
        right = object.right - object.left + left
        if left > self.scrsize[0]:
            right -= GENERAL.GRAPH_WIDTH * self.scrsize[0]
        if right < 0:
            return
        center = list(object.center.t())
        center[0] = center[0] + right - object.right

        rpos = UseCase.Entity.Pos(self.controller.pos.x + GENERAL.GRAPH_WIDTH * self.scrsize[0],self.controller.pos.y,self.controller.pos.stx,self.controller.pos.sty)
        lpos = UseCase.Entity.Pos(self.controller.pos.x - GENERAL.GRAPH_WIDTH * self.scrsize[0],self.controller.pos.y,self.controller.pos.stx,self.controller.pos.sty)
        dist = min(self.controller.pos - object.center,rpos - object.center,lpos - object.center)
        linecolor = color_adapt(GALAXY.LINE_COLOR,GENERAL.BG_COLOR,UseCase.var.alpha,GALAXY.LINE_SHOW_FACTOR,dist)
        fontcolor = color_adapt(GALAXY.LABEL_COLOR,GENERAL.BG_COLOR,UseCase.var.alpha,GALAXY.LABEL_SHOW_FACTOR,dist)
        galnamesurf = self.namefont.get().render(object.name,1,fontcolor)
        if not object.label:
            self.display.blit(galnamesurf,centrialize(*center,*galnamesurf.get_size(),0,0))
        else:
            labelsurf = self.labelfont.get().render(object.label,1,fontcolor)
            scaled = pygame.transform.smoothscale_by(labelsurf,min(2 * object.r / labelsurf.get_width(),1))
            self.display.blit(galnamesurf,centrialize(*center,*galnamesurf.get_size(),0,-GALAXY.LABEL_DISPSIZE/2))
            self.display.blit(scaled,centrialize(*center,*scaled.get_size(),0,GALAXY.LABEL_DISPSIZE/2))
        pygame.draw.aalines(self.display,linecolor,False,[(t[0] + right - object.right,t[1]) for t in [i.t() for i in object.lines]])
        for star in object.stars:
            self.sr.render(star)