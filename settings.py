from os.path import isfile
from json import loads
class CONSTANTS:
    VERSION = "1.2.1-260127-beta"
    PACKVER = "1.2-rev1"
    INITIAL_SCRSIZE = [1536,864]
    TICK_SPEED = 60
class DEBUG:
    ...
class GENERAL:
    SPEED_DACAY = 0.95
    BG_COLOR = [0,0,30]
    ALPHA_DACAY = 3
class GALAXY:
    VISIBLE_DISTANCE = 836.66
    LINE_COLOR = [255,255,255]
    LINE_SHOW_FACTOR = 360
    LABEL_DISPSIZE = 100
    LABEL_COLOR = [109,158,235]
    LABEL_SHOW_FACTOR = 255
class STAR:
    RADIUS = 15
    RADIUS_FACTOR = 1.3
    COLOR = [255,255,255]
    LOCKED_COLOR = [128,128,128]
    SHOW_FACTOR = 360
    class HOVER:
        TICK = 30
        SPEED = 0.2
        REG_FACTOR = (1 - 1 / (SPEED * TICK + 1))
class MOUSE:
    COLOR = [255,255,255]
class AUTOPLAY:
    ENABLE = False
    SCROLL_BG_FACTOR = 0.2
    class TIME:
        MOVEMOUSE = 1
        FADE = 1.5
        CACHE = 0.5
    class MOUSE:
        TICK = None
        SPEED = 0.1
        REG_FACTOR = None
class METEOR:
    ENABLE = True
    LENGTH = [300,600]
    STAY_TICK = 120    # >=slide_tick
    SLIDE_TICK = 90
    COLOR = [255,255,255]
    SHOW_FACTOR = 360
    FRONT_STAR_RADIUS = 15
    BACK_STAR_RADIUS = 12
    ROTATION = 3
    FRONT_COVER_RADIUS = 20
    BACK_COVER_RADIUS = 16
    MIN_PERIOD = 300
    MAX_PERIOD = 1200
    MIN_COUNT = 50
    MAX_COUNT = 250
if isfile("properties"):
    with open("properties") as file:
        section = "GENERAL"
        for i in file.readlines():
            line = i.strip("\n")
            if line in ["[DEBUG]","[GENERAL]","[GALAXY]","[STAR]","[MOUSE]","[AUTOPLAY]","[METEOR]"]:
                section = line.replace("[","").replace("]","")
                continue
            if not "=" in line:
                raise ValueError("Invalid assignment statement in properties.")
            [dest,value] = line.split("=",1)
            try:
                value = loads(value)
            except:
                raise ValueError("Invalid assignment statement in properties.")
            dest = dest.split(".")
            variable = globals()[section]
            for x in dest[:-1]:
                if hasattr(variable,x):
                    variable = getattr(variable,x)
                else:
                    raise ValueError("Invalid assignment statement in properties.")
            if hasattr(variable,dest[-1]):
                setattr(variable,dest[-1],value)
            else:
                raise ValueError("Invalid assignment statement in properties.")
AUTOPLAY.MOUSE.TICK = (AUTOPLAY.TIME.MOVEMOUSE + AUTOPLAY.TIME.FADE - AUTOPLAY.TIME.CACHE) * CONSTANTS.TICK_SPEED
AUTOPLAY.MOUSE.REG_FACTOR = (1 - 1 / (AUTOPLAY.MOUSE.SPEED * AUTOPLAY.MOUSE.TICK + 1))