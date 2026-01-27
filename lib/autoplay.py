from settings import *
from .uimath import scrolling_asdelta
def bgm_val(sec,starcnt):
    sec -= AUTOPLAY.TIME.MOVEMOUSE * starcnt + (AUTOPLAY.TIME.FADE * 2) * starcnt + AUTOPLAY.TIME.FADE
    sec /= starcnt
    if sec > 4 or sec < 1:
        return -1,0
    return 5 - sec - 1 / sec,sec
def schedule(starcnt,dispsec):
    time = 0
    sch = []
    sch.append((time,"move"))
    for i in range(starcnt):
        time += AUTOPLAY.TIME.FADE
        time += AUTOPLAY.TIME.MOVEMOUSE
        sch.append((time,"click"))
        time += AUTOPLAY.TIME.FADE
        sch.append((time,"checkbg"))
        time += dispsec
        sch.append((time,"click"))
        sch.append((time,"move"))
    sch.pop()
    time += AUTOPLAY.TIME.FADE
    sch.append((time,"quit"))
    return sch
class Autoscroll_handler:
    tick = 0
    scrolling = False
    delta = 0
    def __init__(self,dispsec):
        self.maxtick = (dispsec - AUTOPLAY.TIME.CACHE) * CONSTANTS.TICK_SPEED
    def scroll(self,delta):
        self.delta = delta
        self.scrolling = True
    def speed(self):
        if not self.scrolling:
            return 0
        else:
            s = scrolling_asdelta(self.tick,self.maxtick,self.delta)
            self.tick += 1
            if self.tick > self.maxtick:
                self.scrolling = False
                self.tick = 0
            return -s