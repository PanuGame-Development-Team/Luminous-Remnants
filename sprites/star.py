import pygame
from lib import *
from random import randint,choice
class Star(pygame.sprite.Sprite):
    def __init__(self,resource_id,pos,*groups):
        super().__init__(*groups)
        self.resource_id = resource_id
        self.pos = pos
        self.angle = randint(0,359)
        self.rotation = choice([-1,1])
    def update(self,screen,speed,mousepos):
        self.angle += self.rotation
        
        pygame.draw.lines(screen,[255,255,255],1,starposls(5,25,0,100,100))