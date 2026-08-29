import math
from settings import *
from entity.lib import Pos
from random import random
def starposls(n,r,ang,offx,offy):
    ls = []
    ang = ang / 180 * math.pi - math.pi / 2
    dang = (n-1) * math.pi / n
    for i in range(n):
        ls.append((r * math.cos(ang) + offx,r * math.sin(ang) + offy))
        ang += dang
    return ls
def color_adapt(fg,bg,alpha,factor,dist):
    return [(i[0] - i[1]) * (factor - alpha) / factor
             * max(GENERAL.VISIBLE_DISTANCE**2 - dist,0) / GENERAL.VISIBLE_DISTANCE**2 + i[1]
             for i in zip(fg,bg)]
def approaching(hovertick,min,max,CONSTOBJ):            # Deprecated!
    return (1 - 1 / (CONSTOBJ.SPEED * hovertick + 1)) / CONSTOBJ.REG_FACTOR * (max - min)
def centrialize(x1,y1,x2,y2,xoffset,yoffset):
    return [x1 - x2 / 2 + xoffset,y1 - y2 / 2 + yoffset]
def section_formula(x1,y1,x2,y2,factor):
    return [(x2 - x1) * factor + x1,(y2 - y1) * factor + y1]
def sine_approaching(tick,maxtick,delta):
    return math.sin(((tick) / (maxtick + 1) - 0.5) * math.pi) * delta / 2 + delta / 2
def circle_border(radius,centerx,centery,destx,desty):
    pol = Pos(centerx,centery).d(Pos(destx,desty)) / radius
    return [centerx + (destx - centerx) / pol,centery + (desty - centery) / pol]
def period_secion(val,max,min,period):
    return (math.sin(val / period * 2 * math.pi) + 1) / 2 * (max - min) + min
def randlr(min,max):
    return random() * (max - min) + min