import pygame
from lib import *
from settings import *
class Galaxy(pygame.sprite.Sprite):
    def __init__(self,name,label,center,sidls,stars,labelfont,screensize,*groups):
        super().__init__(*groups)
        self.name = name
        self.label = label
        self.center = center
        self.sidls = sidls
        self.stars = pygame.sprite.Group(stars)
        self.left = 1e20
        self.right = -1e20
        for star in self.stars.sprites():
            self.left = min(self.left,star.pos[0] - 15)
            self.right = max(self.right,star.pos[0] + 15)
        self.labelfont = labelfont
        self.screensize = screensize
    def update(self,screen,speed,mouse,alpha):
        for vertex in self.sidls:
            vertex[0] += speed
        self.center[0] += speed
        self.left += speed
        self.right += speed
        dist = calc_distance_sq(*mouse.pos,*self.center)
        linecolor = color_adapt(LINE_COLOR,BG_COLOR,alpha,LINE_SHOW_FACTOR,dist)
        fontcolor = color_adapt(LABEL_COLOR,BG_COLOR,alpha,LABEL_SHOW_FACTOR,dist)
        galnamesurf = self.labelfont.render(self.name,1,fontcolor)
        if not self.label:
            screen.blit(galnamesurf,centrialize(*self.center,*galnamesurf.get_size(),0,0))
        else:
            labelsurf = self.labelfont.render(self.label,1,fontcolor)
            screen.blit(galnamesurf,centrialize(*self.center,*galnamesurf.get_size(),0,-LABEL_DISPSIZE/2))
            screen.blit(labelsurf,centrialize(*self.center,*labelsurf.get_size(),0,LABEL_DISPSIZE/2))
        pygame.draw.aalines(screen,linecolor,False,self.sidls)
        in_screen = self.left < self.screensize[0] and self.right > 0
        self.stars.update(screen,speed,alpha,in_screen,mouse)
        if not in_screen:
            if self.center[0] > self.screensize[0]:
                for vertex in self.sidls:
                    vertex[0] -= self.screensize[0] * 2
                self.center[0] -= self.screensize[0] * 2
                self.left -= self.screensize[0] * 2
                self.right -= self.screensize[0] * 2
            elif self.center[0] < 0:
                for vertex in self.sidls:
                    vertex[0] += self.screensize[0] * 2
                self.center[0] += self.screensize[0] * 2
                self.left += self.screensize[0] * 2
                self.right += self.screensize[0] * 2