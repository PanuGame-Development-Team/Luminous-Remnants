from usecase.usecase import UseCase
from adapter.settings import *
import pygame
class KeyDown(UseCase.Event):
    type = pygame.KEYDOWN
    def __init__(self,eventkey):
        if eventkey == pygame.K_LEFT:
            self.msg = "l"
        elif eventkey == pygame.K_RIGHT:
            self.msg = "r"
        else:
            self.msg = "o"
class KeyUp(UseCase.Event):
    type = pygame.KEYUP
    def __init__(self,eventkey):
        if eventkey == pygame.K_LEFT:
            self.msg = "l"
        elif eventkey == pygame.K_RIGHT:
            self.msg = "r"
        else:
            self.msg = "o"
class MouseMove(UseCase.Event):
    type = pygame.MOUSEMOTION
    def __init__(self,screensize):
        self.msg = UseCase.Entity.Pos(*pygame.mouse.get_pos(),*screensize)
class MouseDown(UseCase.Event):
    type = pygame.MOUSEBUTTONDOWN
    def __init__(self,screensize):
        self.msg = (UseCase.Entity.Pos(*pygame.mouse.get_pos(),*screensize))
class Tick(UseCase.Event):
    type = "Tick"
    def __init__(self,process):
        self.msg = process