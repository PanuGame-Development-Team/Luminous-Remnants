from usecase.usecase import UseCase
from adapter.settings import CONTROLLER,GENERAL
class Controller(UseCase.Controller):
    hover_star = None
    rotate_tick = 0
    rotating = False
    def __init__(self,pos,galaxyls,screensize):
        super().__init__(pos)
        self.galaxyls = galaxyls
        self.screensize = screensize
    def click(self):
        if not self.rotating:
            self.rotating = True
            self.rotate_tick = 0
        if self.showing:
            self.hover_star.pic.stop()
            self.set_pos(self.pos)
        elif self.hover_star:
            self.hover_star.dehover()
            self.hover_star.pic.play()
            self.showing = True
    def set_pos(self,pos):
        pos.x %= GENERAL.GRAPH_WIDTH * self.screensize[0]
        if not self.showing:
            mstar = None
            mdissq = 1e9
            for p in self.galaxyls:
                galaxy = p.get()
                for star in galaxy.stars:
                    if star.locked:
                        continue
                    lpos = UseCase.Entity.Pos(star.pos.x - GENERAL.GRAPH_WIDTH * self.screensize[0],star.pos.y,*self.screensize)
                    rpos = UseCase.Entity.Pos(star.pos.x + GENERAL.GRAPH_WIDTH * self.screensize[0],star.pos.y,*self.screensize)
                    distance = min(star.pos - self.pos,rpos - self.pos,lpos - self.pos)
                    if distance < min(CONTROLLER.HOVER_DISTANCE_SQ,mdissq):
                        mstar = star
                        mdissq = distance
            if self.hover_star != mstar:
                if self.hover_star:
                    self.hover_star.dehover()
                self.hover_star = mstar
                if mstar:
                    mstar.hover()
        return super().set_pos(pos)
    def tick(self):
        if self.rotating:
            self.rotate_tick += 1
            if self.rotate_tick > CONTROLLER.ROTATE_TICK:
                self.rotate_tick = 0
                self.rotating = False
        if self.showing:
            self.showing = self.hover_star.pic.showing
            if not self.showing:
                self.hover_star = None
                self.set_pos(self.get_pos())