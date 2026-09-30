from entity import settings as eset
from usecase import settings as uset
from adapter import settings as aset
from settings import *

METEOR.ENABLE = False
GENERAL.VISIBLE_DISTANCE = 1e9

eset.DEBUG = DEBUG
eset.STAR = STAR
uset.PICTURE = PICTURE
uset.STAR = STAR
uset.METEOR = METEOR
uset.DEBUG = DEBUG
aset.CONTROLLER = CONTROLLER
aset.HANDLER = HANDLER
aset.CONSTANTS = CONSTANTS
# aset.CONTROLLER = CONTROLLER
aset.GALAXY = GALAXY
aset.GENERAL = GENERAL
# aset.HANDLER = HANDLER
aset.STAR = STAR

from init import loadall
from json import dumps
from adapter.pygame.data_provider_pickle import Pickle
from adapter.pygame.renderer.renderer_controller import ControllerRenderer
from adapter.pygame.renderer.renderer_star import StarRenderer
from adapter.pygame.renderer.renderer_galaxy import GalaxyRenderer
from adapter.pygame.handler_mousekbd import MouseKBD
from adapter.pygame.renderer.uimath import find_nearest
from adapter.controller import Controller
from usecase.usecase import UseCase
from adapter.pygame.events import *

class InjectedPicture(UseCase.Picture):
    def __init__(self,starindex,handler):
        super().__init__(None)
        self.starindex = starindex
        self.handler = handler
    def play(self):
        self.showing = True
        self.alpha = PICTURE.MAX_ALPHA / 2
        handler.edit_star(self.starindex)
    def stop(self):
        return
class InjectedGalaxyRenderer(GalaxyRenderer):
    def render(self,object:UseCase.Galaxy,hover=False,noalpha=False):
        if noalpha:
            alpha = UseCase.var.alpha
            UseCase.var.alpha = 0
        super().render(object)
        if noalpha:
            UseCase.var.alpha = alpha
        if hover:
            left = (object.left + UseCase.var.scroffset) % (GENERAL.GRAPH_WIDTH * self.scrsize[0])
            right = object.right - object.left + left
            if left > self.scrsize[0]:
                right -= GENERAL.GRAPH_WIDTH * self.scrsize[0]
            if right < 0:
                return
            left = object.left + right - object.right
            pygame.draw.line(self.display,[255,255,255],[left,0],[left,screensize[1]],3)
            pygame.draw.line(self.display,[255,255,255],[right,0],[right,screensize[1]],3)
class InjectedHandler(MouseKBD):
    state = 0       # 0:select 1:galaxy 2:star
    galaxyname = ""
    starindex = 0
    star_posid = {}
    down = {}
    injected_reg = UseCase.Entity.ResourceManager()
    def __init__(self,controller,galaxydict,galaxy,screensize):
        super().__init__(controller)
        self.galaxydict = galaxydict
        self.galaxy = galaxy
        self.screensize = screensize
        self.change_state(0)
        for galaxyname in galaxydict:
            formatted = [[UseCase.Entity.Pos(*stardat["pos"],*GENERAL.INITIAL_SCRSIZE).scale(*self.screensize),stardat["star"]] for stardat in galaxydict[galaxyname][:-1]]
            starcnt = 0
            i = 0
            for stardat in formatted:
                if stardat[1]:
                    self.star_posid[(galaxyname,starcnt)] = i
                    starcnt += 1
                i += 1
    def emit(self,event):
        if event.type == Tick.type:
            if self.state == 0:
                self.galaxyname = find_nearest(self.controller.pos,galaxyls,lambda x:x.get().center,lambda x:x.get().name)[1]
            elif self.state == 1:
                delta = [0,0]
                if self.down.get(pygame.K_a):
                    delta[0] -= 1
                if self.down.get(pygame.K_d):
                    delta[0] += 1
                if self.down.get(pygame.K_w):
                    delta[1] -= 1
                if self.down.get(pygame.K_s) and not self.down.get(pygame.K_w):
                    delta[1] += 1
                if delta[0] != 0 or delta[1] != 0:
                    for t in self.galaxydict[self.galaxyname][:-1]:
                        t["pos"][0] += delta[0]
                        t["pos"][1] += delta[1]
                    for i in range(len(self.galaxy[self.galaxyname].get().stars)):
                        self.galaxy[self.galaxyname].get().stars[i].pos = UseCase.Entity.Pos(*self.galaxydict[self.galaxyname][self.star_posid[self.galaxyname,i]]["pos"],*GENERAL.INITIAL_SCRSIZE).scale(*screensize)
                    self.reload_galaxy()
            elif self.state == 2:
                op = False
                if self.down.get(pygame.K_a) and not self.down.get(pygame.K_d):
                    self.galaxydict[self.galaxyname][self.star_posid[self.galaxyname,self.starindex]]["pos"][0] -= 1
                    op = True
                if self.down.get(pygame.K_d) and not self.down.get(pygame.K_a):
                    self.galaxydict[self.galaxyname][self.star_posid[self.galaxyname,self.starindex]]["pos"][0] += 1
                    op = True
                if self.down.get(pygame.K_w) and not self.down.get(pygame.K_s):
                    self.galaxydict[self.galaxyname][self.star_posid[self.galaxyname,self.starindex]]["pos"][1] -= 1
                    op = True
                if self.down.get(pygame.K_s) and not self.down.get(pygame.K_w):
                    self.galaxydict[self.galaxyname][self.star_posid[self.galaxyname,self.starindex]]["pos"][1] += 1
                    op = True
                if op:
                    self.galaxy[self.galaxyname].get().stars[self.starindex].pos = UseCase.Entity.Pos(*self.galaxydict[self.galaxyname][self.star_posid[self.galaxyname,self.starindex]]["pos"],*GENERAL.INITIAL_SCRSIZE).scale(*screensize)
                    self.reload_galaxy()
        elif event.type == MouseDown.type:
            if self.state == 0:
                self.change_state(1)
            elif self.state == 2:
                starls = self.galaxy[self.galaxyname].get().stars
                lstarls = starls[:]
                c_star = lstarls.pop(self.starindex)
                dis,star = find_nearest(self.controller.pos,lstarls,lambda x:x.pos)
                if dis <= (STAR.RADIUS + CONTROLLER.RADIUS) ** 2:
                    starindex = None
                    c_starindex = None
                    for i in range(len(starls)):
                        starpos = UseCase.Entity.Pos(*self.galaxydict[self.galaxyname][self.star_posid[self.galaxyname,i]]["pos"],*GENERAL.INITIAL_SCRSIZE).scale(*screensize)
                        if star.pos.x == starpos.x and star.pos.y == starpos.y:
                            starindex = i
                        if c_star.pos.x == starpos.x and c_star.pos.y == starpos.y:
                            c_starindex = i
                    if c_starindex != starindex:
                        if c_starindex + 1 and starindex + 1:
                            self.galaxydict[self.galaxyname][-1].append([self.star_posid[self.galaxyname,starindex],self.star_posid[self.galaxyname,c_starindex]])
                        else:
                            raise ValueError("Galaxydict and handler.galaxy not synchorized.")
                else:
                    pos = self.controller.get_pos()
                    starindex = len(self.galaxy[self.galaxyname].get().stars)
                    self.galaxy[self.galaxyname].get().stars.append(UseCase.Star(0,1,pos,True,None))
                    posindex = len(self.galaxydict[self.galaxyname]) - 1
                    pos = pos.copy().scale(*GENERAL.INITIAL_SCRSIZE)
                    self.galaxydict[self.galaxyname].insert(-1,{"pos":list(pos.t()),"star":True})
                    self.star_posid[self.galaxyname,starindex] = posindex
                self.reload_galaxy()
        elif event.type == KeyDown.type:
            self.down[event.msg] = True
            if event.msg == pygame.K_SPACE:
                if self.state == 0:
                    self.galaxyname = self.get_name()
                    pos = self.controller.get_pos()
                    star = UseCase.Star(0,1,pos,True,None)
                    self.galaxy[self.galaxyname] = self.injected_reg.register(UseCase.Galaxy(self.galaxyname,None,[star],[]))
                    self.galaxydict[self.galaxyname] = [{"pos":star.pos.copy().scale(*GENERAL.INITIAL_SCRSIZE).t(),"star":True},[]]
                    galaxyls.append(self.galaxy[self.galaxyname])
                    self.star_posid[self.galaxyname,0] = 0
                    self.change_state(1)
                    self.controller.set_pos(self.controller.pos)
                    self.controller.click()
                elif self.state == 1:
                    self.change_state(0)
                elif self.state == 2:
                    self.change_state(1)
            if event.msg == pygame.K_DELETE:
                if self.state == 1:
                    self.galaxy.pop(self.galaxyname)
                    self.change_state(0)
                if self.state == 2:
                    self.galaxydict[self.galaxyname][self.star_posid[self.galaxyname,self.starindex]]["star"] = False
                    for i in self.galaxydict[self.galaxyname][-1][:]:
                        if i[0] == self.star_posid[self.galaxyname,self.starindex] or i[1] == self.star_posid[self.galaxyname,self.starindex]:
                            self.galaxydict[self.galaxyname][-1].remove(i)
                    self.galaxy[self.galaxyname].get().stars.pop(self.starindex)
                    self.controller.showing = False
                    self.controller.hover_star = None
                    self.controller.set_pos(self.controller.pos)
                    if self.galaxy[self.galaxyname].get().stars:
                        self.reload_galaxy()
                        self.change_state(1,False)
                        for i in range(len(self.galaxy[self.galaxyname].get().stars)):
                            if i >= self.starindex:
                                self.star_posid[self.galaxyname,i] = self.star_posid[self.galaxyname,i+1]
                        self.star_posid.pop(self.galaxyname,len(self.galaxy[self.galaxyname].get().stars))
                    else:
                        self.galaxy.pop(self.galaxyname)
                        self.galaxydict.pop(self.galaxyname)
                        self.change_state(0,False)
        elif event.type == KeyUp.type:
            self.down[event.msg] = False
        return super().emit(event)
    def change_state(self,to,stop=True):
        if stop and self.state == 2 and to != 2:
            self.galaxy[self.galaxyname].get().stars[self.starindex].pic.showing = False
        if to == 0:
            for galaxy in galaxyls:
                for star in galaxy.get().stars:
                    star.pic = None
                    star.locked = True
            UseCase.var.alpha = 0
        elif to == 1:
            if not self.galaxyname in self.galaxy:
                return
            galaxy = self.galaxy[self.galaxyname].get()
            for i in range(len(galaxy.stars)):
                star = galaxy.stars[i]
                star.pic = InjectedPicture(i,self)
                star.locked = False
                star.rotation = 1
            UseCase.var.alpha = PICTURE.MAX_ALPHA / 2
        elif to == 2:
            for galaxy in galaxyls:
                for i in range(len(galaxy.get().stars)):
                    star = galaxy.get().stars[i]
                    if self.starindex != i or galaxy.get().name != self.galaxyname:
                        star.pic = None
                        star.locked = True
                    else:
                        star.locked = False
            UseCase.var.alpha = 0
        self.state = to
    def edit_star(self,starindex):
        self.starindex = starindex
        self.change_state(2)
    def reload_galaxy(self):
        formatted = [[UseCase.Entity.Pos(*stardat["pos"],*GENERAL.INITIAL_SCRSIZE).scale(*self.screensize),stardat["star"]] for stardat in self.galaxydict[self.galaxyname][:-1]]
        galaxy = self.galaxy[self.galaxyname].get()
        lines = [[formatted[i[0]][0],formatted[i[1]][0]] for i in self.galaxydict[self.galaxyname][-1]]
        galaxy.__init__(galaxy.name,galaxy.label,galaxy.stars,lines)
    def get_name(self):
        i = 1
        while f"UNNAME {i}" in self.galaxy:
            i += 1
        return f"UNNAME {i}"
import pygame
pygame.init()
screen = pygame.display.set_mode([1280,720] if DEBUG.WINDOW else [0,0],pygame.FULLSCREEN if not DEBUG.WINDOW else 0)
clock = pygame.time.Clock()
screensize = screen.get_size()
pygame.mouse.set_visible(False)
dataprovider = Pickle(screensize,"main.lrg")
footnotes = [CONSTANTS.VERSION,CONSTANTS.APP_NAME,"NO METEOR","Graph Editor"]
if not loadall(screen,dataprovider,clock,footnotes):
    quit(0)
galaxyls = [i[1] for i in dataprovider.resource("galaxy").items()]
controller = Controller(UseCase.Entity.Pos(*pygame.mouse.get_pos(),*screensize),galaxyls,screensize)
handler = InjectedHandler(controller,dataprovider.dic["星座/galaxy.json"],dataprovider.resource("galaxy"),screensize)
sr = StarRenderer(screen,screensize)
gr = InjectedGalaxyRenderer(screen,screensize,controller,dataprovider.resource("namefont"),dataprovider.resource("labelfont") if dataprovider.resource("labelfont") else dataprovider.resource("namefont"),sr)
cr = ControllerRenderer(screen,screensize)
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
                handler.emit(MouseDown(screensize))
            elif event.type == pygame.MOUSEMOTION:
                handler.emit(MouseMove(screensize))
    except UseCase.StopPlaying:
        keepgoing = False
    screen.fill(GENERAL.BG_COLOR)
    for galaxyname in dataprovider.resource("galaxy"):
        dataprovider.resource("galaxy")[galaxyname].get().tick()
    for galaxyname in dataprovider.resource("galaxy"):
        if handler.state == 0:
            gr.render(dataprovider.resource("galaxy")[galaxyname].get(),galaxyname==handler.galaxyname)
        elif handler.state == 1 or handler.state == 2:
            gr.render(dataprovider.resource("galaxy")[galaxyname].get(),noalpha=galaxyname==handler.galaxyname)
    cr.render(controller)
    pygame.display.update()
    clock.tick(CONSTANTS.TICK_SPEED)
pygame.quit()
with open("test.json","w") as file:
    file.write(dumps(handler.galaxydict,ensure_ascii=False))