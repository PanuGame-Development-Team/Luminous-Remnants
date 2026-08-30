from usecase.usecase import UseCase
from adapter.pygame.events import Tick
from adapter.settings import HANDLER,CONSTANTS
from adapter.pygame.renderer.uimath import *
import pygame
class AutoplayStarCountOutOfRange(Exception):...
class Autoplay(UseCase.Handler):
    sched = []
    process = None
    tick = 0
    dest = [-1,0]
    def __init__(self,controller,bgmls:list[tuple[str,UseCase.Entity.Resource_id]],galaxyls:list[UseCase.Entity.Resource_id],screensize):
        super().__init__(controller)
        self.screensize = screensize
        self.galaxyls = galaxyls
        starcnt = 0
        for galaxy in self.galaxyls:
            for star in galaxy.get().stars:
                if not star.locked:
                    starcnt += 1
        ls = []
        for path,bgm in bgmls:
            ls += [(bgm,*self.bgm_val(bgm.get().get_length() * loop,starcnt),path) for loop in range(1,HANDLER.AUTOPLAY.MAX_LOOP + 1)]
        bgm,score,self.dispsec,path = sorted(ls,key=lambda x:x[1],reverse=True)[0]
        if score == -1:
            raise AutoplayStarCountOutOfRange("The background musics included cannot support autoplay.Try to add more.")
        self.schedule(starcnt)
        pygame.mixer.music.load(path)
    def bgm_val(self,sec:float,starcnt:int):
        sec -= HANDLER.AUTOPLAY.TIME.MOVEMOUSE * starcnt + (HANDLER.AUTOPLAY.TIME.FADE * 2) * starcnt + HANDLER.AUTOPLAY.TIME.FADE
        sec /= starcnt
        if sec > 4 or sec < 1:
            return -1,0
        return 5 - sec - 1 / sec,sec
    def schedule(self,starcnt:int):
        time = 0
        self.sched.append([time,"move"])
        for i in range(starcnt):
            time += HANDLER.AUTOPLAY.TIME.FADE
            time += HANDLER.AUTOPLAY.TIME.MOVEMOUSE
            self.sched.append([time,"click"])
            time += HANDLER.AUTOPLAY.TIME.FADE
            self.sched.append([time,"checkbg"])
            time += self.dispsec
            self.sched.append([time,"click"])
            self.sched.append([time,"move"])
        self.sched.pop()
        time += HANDLER.AUTOPLAY.TIME.FADE
        self.sched.append([time,"quit"])
        self.next()
    def step(self):
        self.dest[1] += 1
        if self.dest[1] >= len(self.galaxyls[self.dest[0]].get().stars):
            self.dest[1] = 0
            self.dest[0] += 1
            if self.dest[0] >= len(self.galaxyls):
                self.dest[0] = 0
    def next(self):
        if self.dest[0] == -1:
            self.dest = [0,-1]
        self.step()
        while self.galaxyls[self.dest[0]].get().stars[self.dest[1]].locked:
            self.step()
    def emit(self,event:UseCase.Event):
        if event.type == Tick.type:
            if self.sched and pygame.mixer.music.get_pos() / 1000 >= self.sched[0][0]:
                self.process = self.sched.pop(0)
            if self.process:
                if self.process[1] == "click":
                    self.controller.click()
                    self.process = None
                elif self.process[1] == "quit":
                    raise UseCase.StopPlaying("Stop playing.")
                elif self.process[1] == "checkbg":
                    self.next()
                    gal = self.galaxyls[self.dest[0]].get()
                    if gal.right + UseCase.var.scroffset > self.screensize[0] * (1 - HANDLER.AUTOPLAY.SCROLL_BG_FACTOR):
                        self.process = [None,"scroll",(gal.left + UseCase.var.scroffset - self.screensize[0] * HANDLER.AUTOPLAY.SCROLL_BG_FACTOR),UseCase.var.scroffset]
                    else:
                        self.process = None
                elif self.process[1] == "scroll":
                    maxtick = (self.dispsec - HANDLER.AUTOPLAY.TIME.CACHE) * CONSTANTS.TICK_SPEED
                    self.tick += 1
                    if self.tick > maxtick:
                        self.tick = 0
                        self.process = None
                        return
                    UseCase.var.scroffset = self.process[3] - sine_slide(self.tick,maxtick,self.process[2])
                    self.controller.pos.x += sine_slide(self.tick,maxtick,self.process[2]) - sine_slide(self.tick - 1,maxtick,self.process[2])
                elif self.process[1] == "move":
                    maxtick = (HANDLER.AUTOPLAY.TIME.MOVEMOUSE + HANDLER.AUTOPLAY.TIME.FADE - HANDLER.AUTOPLAY.TIME.CACHE) * CONSTANTS.TICK_SPEED
                    self.tick += 1
                    if self.tick > maxtick:
                        self.tick = 0
                        self.process = None
                        return
                    if len(self.process) == 2:
                        self.process.append(self.controller.get_pos())
                    star = self.galaxyls[self.dest[0]].get().stars[self.dest[1]]
                    lpos = UseCase.Entity.Pos(star.pos.x - GENERAL.GRAPH_WIDTH * self.screensize[0],star.pos.y,*self.screensize)
                    rpos = UseCase.Entity.Pos(star.pos.x + GENERAL.GRAPH_WIDTH * self.screensize[0],star.pos.y,*self.screensize)
                    nearestpos = sorted([(i - self.process[2],i) for i in [star.pos,lpos,rpos]])[0][1]
                    pos = section_formula(*self.process[2].t(),
                                          *nearestpos.t(),
                                          approaching(self.tick,maxtick,0,1))
                    self.controller.set_pos(UseCase.Entity.Pos(*pos,*self.screensize))
            self.controller.set_pos(self.controller.get_pos())
            self.controller.tick()