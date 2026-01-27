from settings import AUTOPLAY
def bgm_val(sec,starcnt):
    sec -= AUTOPLAY.TIME.MOVEMOUSE * starcnt + (AUTOPLAY.TIME.FADE * 2 + 1) * starcnt
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