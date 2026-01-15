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
             * max(VISIBLE_DISTANCE**2 - dist,0) / VISIBLE_DISTANCE**2 + i[1]
             for i in zip(fg,bg)]
def calc_distance_sq(x1,y1,x2,y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2
def centrialize(x1,y1,x2,y2,xoffset,yoffset):
    return [x1 - x2 / 2 + xoffset,y1 - y2 / 2 + yoffset]