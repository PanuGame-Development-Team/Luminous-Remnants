from entity import settings as eset
from usecase import settings as uset
from adapter import settings as aset
from settings import *
eset.DEBUG = DEBUG
eset.STAR = STAR
uset.PICTURE = PICTURE
uset.STAR = STAR
uset.METEOR = METEOR
aset.CONTROLLER = CONTROLLER
aset.HANDLER = HANDLER
aset.CONSTANTS = CONSTANTS
# aset.CONTROLLER = CONTROLLER
aset.GALAXY = GALAXY
aset.GENERAL = GENERAL
# aset.HANDLER = HANDLER
aset.STAR = STAR

from init import loadall
from adapter.pygame.data_provider_pickle import Pickle
from adapter.pygame.renderer.renderer_controller import ControllerRenderer
from adapter.pygame.renderer.renderer_picture import PictureRenderer
from adapter.pygame.renderer.renderer_star import StarRenderer
from adapter.pygame.renderer.renderer_galaxy import GalaxyRenderer
from adapter.pygame.renderer.renderer_meteor import MeteorRenderer,MeteorRainProcesser
from adapter.pygame.handler_mousekbd import MouseKBD
from adapter.pygame.handler_autoplay import Autoplay
from adapter.controller import Controller
from usecase.usecase import UseCase
from adapter.pygame.events import *
import pygame
pygame.init()
screen = pygame.display.set_mode([1280,720] if DEBUG.WINDOW else [0,0],pygame.FULLSCREEN if not DEBUG.WINDOW else 0)
clock = pygame.time.Clock()
screensize = screen.get_size()
pygame.mouse.set_visible(False)
dataprovider = Pickle(screensize,"main.lrg")
footnotes = [CONSTANTS.VERSION,CONSTANTS.APP_NAME]
if HANDLER.AUTOPLAY.ENABLE:
    footnotes.append("AUTOPLAY")
if not METEOR.ENABLE:
    footnotes.append("NO METEOR")
if not loadall(screen,dataprovider,clock,footnotes):
    quit(0)
galaxyls = [i[1] for i in dataprovider.resource("galaxy").items()]
if not HANDLER.AUTOPLAY.ENABLE:
    controller = Controller(UseCase.Entity.Pos(*pygame.mouse.get_pos(),*screensize),galaxyls,screensize)
    handler = MouseKBD(controller)
    bgm = dataprovider.resource("bgm")[0].get().play(-1)
else:
    controller = Controller(UseCase.Entity.Pos(screensize[0] / 2,screensize[1] / 2,*screensize),galaxyls,screensize)
    handler = Autoplay(controller,list(zip(dataprovider.path["bgm"],dataprovider.resource("bgm"))),galaxyls,screensize)
    pygame.mixer.music.play(-1)
pr = PictureRenderer(screen,screensize)
sr = StarRenderer(screen,screensize)
gr = GalaxyRenderer(screen,screensize,controller,dataprovider.resource("namefont"),sr)
cr = ControllerRenderer(screen,screensize,pr)
mr = MeteorRenderer(screen,screensize)
meteorls = []
rain_processer = MeteorRainProcesser(screensize)
keepgoing = True
while keepgoing:
    try:
        handler.emit(Tick(None))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                handler.emit(KeyDown(event.key))
                if event.key == pygame.K_ESCAPE:
                    keepgoing = False
            elif event.type == pygame.KEYUP:
                handler.emit(KeyUp(event.key))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(controller.pos.t())
                handler.emit(MouseDown(screensize))
            elif event.type == pygame.MOUSEMOTION:
                handler.emit(MouseMove(screensize))
    except UseCase.StopPlaying:
        keepgoing = False
    screen.fill(GENERAL.BG_COLOR)
    for galaxyname in dataprovider.resource("galaxy"):
        dataprovider.resource("galaxy")[galaxyname].get().tick()
    for meteor in meteorls:
        meteor.tick()
    rain_processer.handle(meteorls)
    for galaxyname in dataprovider.resource("galaxy"):
        gr.render(dataprovider.resource("galaxy")[galaxyname].get())
    for meteor in meteorls:
        mr.render(meteor)
    cr.render(controller)
    pygame.display.update()
    clock.tick(CONSTANTS.TICK_SPEED)
pygame.quit()