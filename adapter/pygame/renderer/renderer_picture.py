from usecase.usecase import UseCase
from adapter.settings import *
from adapter.pygame.renderer.uimath import *
import pygame
class PictureRenderer(UseCase.Renderer):
    def __init__(self,display:pygame.surface.Surface,scrsize):
        self.display = display
        self.scrsize = scrsize
    def render(self,object:UseCase.Picture):
        if object.showing:
            pos = centrialize(self.scrsize[0] / 2,self.scrsize[1] / 2,*object.resource_id.get().get_size(),0,0)
            object.resource_id.get().set_alpha(UseCase.var.alpha)
            self.display.blit(object.resource_id.get(),pos)