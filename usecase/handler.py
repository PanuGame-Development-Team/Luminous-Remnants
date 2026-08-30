from ca import *
from usecase.controller import Controller
from usecase.lib import *
class StopPlaying(Exception):...
class Handler(Interface):
    def __init__(self,controller:Controller):
        self.controller = controller
    def emit(self,event:Event):...