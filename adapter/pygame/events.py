from usecase.usecase import UseCase
from adapter.settings import *
import pygame
class KeyDown(UseCase.Event):
    type = 0
    def __init__(self,eventkey):
        self.msg = eventkey
class KeyUp(UseCase.Event):
    type = 1
    def __init__(self,eventkey):
        self.msg = eventkey
class MouseMove(UseCase.Event):
    type = 2
    def __init__(self,screensize):
        self.msg = UseCase.Entity.Pos(*pygame.mouse.get_pos(),*screensize)
class MouseDown(UseCase.Event):
    type = 3
    def __init__(self,screensize):
        self.msg = (UseCase.Entity.Pos(*pygame.mouse.get_pos(),*screensize))
class Tick(UseCase.Event):
    type = 4
    def __init__(self,process):
        self.msg = process