import math as _math
def starposls(n,r,ang,offx,offy):
    ls = []
    ang = ang / 180 * _math.pi - _math.pi / 2
    dang = (n-1) * _math.pi / n
    for i in range(n):
        ls.append((r * _math.cos(ang) + offx,r * _math.sin(ang) + offy))
        ang += dang
    return ls