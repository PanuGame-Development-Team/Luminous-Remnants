import pygame
from lib import *
from random import randint,choice
from settings import *
class Star(pygame.sprite.Sprite):
    def __init__(self,resource_id,pos,screensize,locked,*groups):
        super().__init__(*groups)
        self.resource_id = resource_id
        self.pos = pos
        self.angle = randint(0,359)
        self.rotation = choice([-1,1])
        self.screensize = screensize
    def update(self,screen,speed,alpha,in_screen):
        self.angle += self.rotation
        self.angle %= 360
        self.pos[0] += speed
        if self.pos[0] > self.screensize[0]:
            self.pos[0] -= self.screensize[0] * 2
        elif self.pos[0] < 0:
            self.pos[0] += self.screensize[0] * 2
        if in_screen:
            color = color_adapt(LINE_COLOR,BG_COLOR,alpha,LINE_SHOW_FACTOR,0)
            pygame.draw.aalines(screen,color,1,starposls(5,15,self.angle,*self.pos))