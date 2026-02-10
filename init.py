import pygame
import os
from threading import Thread
from pickle import load as pload
from uuid import uuid4
from settings import *
from sprites.galaxy import Galaxy
from sprites.star import Star
from lib.autoplay import *
from lib import color_adapt
import sys
if not os.path.isdir("temp"):
    os.mkdir("temp")
pygame.init()
def savdat(name,dat):
    filename = "temp/" + uuid4().hex + "." + name.split(".")[-1]
    with open(filename,"wb") as file:
        file.write(dat)
    return filename
def cont2img(index:str,dic:dict):
    filename = savdat(index,dic[index])
    return pygame.image.load(filename).convert_alpha()
def init():
    global galaxy,bgm,labelfont,imgresource,sched,scroller
    with open("main.pdb","rb") as file:
        dic = pload(file)
    if dic.get("VERSION") != CONSTANTS.PACKVER:
        pygame.quit()
        raise Exception("PDB version incompatible.")
    labelfont = pygame.font.Font(savdat("ttf",dic["font.ttf"]),GALAXY.LABEL_DISPSIZE)
    bgm = pygame.mixer.Sound(savdat("ogg",dic["bg.ogg"]))
    galaxy = pygame.sprite.Group()
    imgresource = {}
    startot = 0
    for galaxyname in dic["星座/galaxy.json"]:
        label = dic[f"星座/{galaxyname}/label.txt"]
        center = [0,0]
        scaled = [[int(stardat["pos"][0]/CONSTANTS.INITIAL_SCRSIZE[0]*screensize[0]),int(stardat["pos"][1]/CONSTANTS.INITIAL_SCRSIZE[1]*screensize[1]),stardat["star"]] for stardat in dic["星座/galaxy.json"][galaxyname]]
        starcnt = 0
        stars = []
        for stardat in scaled:
            if stardat[2]:
                starcnt += 1
                center[0] += stardat[0]
                center[1] += stardat[1]
                if f"星座/{galaxyname}/{starcnt}.jpg" in dic:
                    startot += 1
                    select = cont2img(f"星座/{galaxyname}/{starcnt}.jpg",dic).convert()
                    if screensize[0] / select.get_size()[0] > screensize[1] / select.get_size()[1]:
                        scale = screensize[1] / select.get_size()[1]
                    else:
                        scale = screensize[0] / select.get_size()[0]
                    image = pygame.transform.smoothscale(select,[select.get_size()[0]*scale,select.get_size()[1]*scale])
                    imgrid = galaxyname + str(starcnt)
                    imgresource[imgrid] = image
                    stars.append(Star(imgrid,stardat[:2],screensize,False))
                else:
                    stars.append(Star(None,stardat[:2],screensize,True))
        center[0] /= starcnt
        center[1] /= starcnt
        sidls = [stardat[:2] for stardat in scaled]
        galaxy.add(Galaxy(galaxyname,label,center,sidls,stars,labelfont,screensize))
    if AUTOPLAY.ENABLE:
        bgm2 = pygame.mixer.Sound(savdat("ogg",dic["bg2.ogg"]))
        ls = []
        ls.append((bgm_val(bgm.get_length(),startot),bgm))
        ls.append((bgm_val(bgm.get_length() * 2,startot),bgm))
        ls.append((bgm_val(bgm2.get_length(),startot),bgm2))
        ls.append((bgm_val(bgm2.get_length() * 2,startot),bgm2))
        val,bgm = max(*ls,key=lambda x:x[0][0])
        if val[0] == -1:
            raise ValueError("Stars are not enough to support autoplay.")
        sched = schedule(startot,val[1])
        scroller = Autoscroll_handler(val[1])
screen = pygame.display.set_mode([0,0],pygame.DOUBLEBUF|pygame.HWSURFACE|pygame.FULLSCREEN,8)
# screen = pygame.display.set_mode([1024,768])
pygame.event.set_allowed([pygame.KEYDOWN,pygame.KEYUP,pygame.MOUSEBUTTONDOWN])
screensize = screen.get_size()
keepgoing = True
first = True
alpha = 0
deltaalpha = GENERAL.ALPHA_DACAY
with open("logo.pdb","rb") as file:
    temp = pload(file)
logo2 = cont2img("logo2.png",temp)
logo = cont2img("logo.png",temp)
clock = pygame.time.Clock()
initd = Thread(target=init)
footnotefont = pygame.font.SysFont("monospace",INIT.FOOTNOTE_FONT_SIZE)
footnotes = [CONSTANTS.VERSION,CONSTANTS.APP_NAME]
if AUTOPLAY.ENABLE:
    footnotes.append("AUTOPLAY")
if not METEOR.ENABLE:
    footnotes.append("NO METEOR")
logo2loc = [(screensize[0]-logo2.get_size()[0])/2,(screensize[1]+logo.get_size()[1])/2]
logoloc = [(screensize[0]-logo.get_size()[0])/2,(screensize[1]-logo.get_size()[1])/2]
while True:
    screen.fill(GENERAL.BG_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    if alpha >= 255 - GENERAL.ALPHA_DACAY + 1:
        if first:
            deltaalpha = 0
            initd.start()
            first = False
        elif not initd.is_alive():
            deltaalpha = -GENERAL.ALPHA_DACAY
    alpha += deltaalpha
    if alpha < 0:
        break
    h = screensize[1]
    for note in footnotes:
        surf = footnotefont.render(note,True,color_adapt(INIT.FOOTNOTE_COLOR,GENERAL.BG_COLOR,255-alpha,255,0))
        h -= surf.get_height()
        screen.blit(surf,[screensize[0] - surf.get_width(),h])
    logo.set_alpha(alpha)
    logo2.set_alpha(alpha)
    screen.blit(logo,logoloc)
    screen.blit(logo2,logo2loc)
    pygame.display.update()
    clock.tick(CONSTANTS.TICK_SPEED)
del init,logo,logo2,initd,surf,footnotefont
pygame.mouse.set_visible(False)