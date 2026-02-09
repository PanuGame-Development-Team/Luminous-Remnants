import math as _math
from settings import *
def starposls(n,r,ang,offx,offy):
    ls = []
    ang = ang / 180 * _math.pi - _math.pi / 2
    dang = (n-1) * _math.pi / n
    for i in range(n):
        ls.append((r * _math.cos(ang) + offx,r * _math.sin(ang) + offy))
        ang += dang
    return ls
def color_adapt(fg,bg,alpha,factor,dist):
    return [(i[0] - i[1]) * (factor - alpha) / factor
             * max(GALAXY.VISIBLE_DISTANCE**2 - dist,0) / GALAXY.VISIBLE_DISTANCE**2 + i[1]
             for i in zip(fg,bg)]
def calc_distance_sq(x1,y1,x2,y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2
def centrialize(x1,y1,x2,y2,xoffset,yoffset):
    return [x1 - x2 / 2 + xoffset,y1 - y2 / 2 + yoffset]
def approaching(hovertick,min,max,CONSTOBJ):
    return (1 - 1 / (CONSTOBJ.SPEED * hovertick + 1)) / CONSTOBJ.REG_FACTOR * (max - min)
def sectionformula(x1,y1,x2,y2,factor):
    return [(x2 - x1) * factor + x1,(y2 - y1) * factor + y1]
def scrolling(tick,maxtick,delta):
    return _math.sin(((tick) / (maxtick + 1) - 0.5) * _math.pi) * delta / 2 + delta / 2
def find_next(dest,galaxy):
    dest[1] += 1
    if dest[1] >= len(galaxy.sprites()[dest[0]].stars.sprites()):
        dest[1] = 0
        dest[0] += 1
        if dest[0] >= len(galaxy.sprites()):
            dest[0] = 0
    while galaxy.sprites()[dest[0]].stars.sprites()[dest[1]].locked:
        dest[1] += 1
        if dest[1] >= len(galaxy.sprites()[dest[0]].stars.sprites()):
            dest[1] = 0
            dest[0] += 1
            if dest[0] >= len(galaxy.sprites()):
                dest[0] = 0
def circle_border(radius,centerx,centery,destx,desty):
    pol = _math.sqrt(calc_distance_sq(centerx,centery,destx,desty)) / radius
    return [centerx + (destx - centerx) / pol,centery + (desty - centery) / pol]