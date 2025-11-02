import pygame
import os
from threading import Thread
from random import randint
from pickle import load as pload
from uuid import uuid4
from settings import *
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
    global imgls,angls,sidls,bgm,star,galaxycenter,galaxylabel,starrotated,labelfont
    with open("main.pdb","rb") as file:
        dic = pload(file)
    if dic.get("VERSION") != PACKVER:
        pygame.quit()
        raise Exception("PDB version incompatible.")
    star4 = cont2img("4.png",dic)
    star5 = cont2img("5.png",dic)
    star6 = cont2img("6.png",dic)
    starlock = cont2img("lock.png",dic)
    star = [star4,star5,star6,starlock]
    starrotated = [[],[],[],[starlock]]
    labelfont = pygame.font.Font(savdat("ttf",dic["font.ttf"]),LABEL_DISPSIZE)
    for angle in range(360):
        starrotated[0].append(pygame.transform.rotate(star4,angle))
        starrotated[1].append(pygame.transform.rotate(star5,angle))
        starrotated[2].append(pygame.transform.rotate(star6,angle))
    bgm = pygame.mixer.Sound(savdat("ogg",dic["bg.ogg"]))
    galaxycenter = {}
    imgls = {}
    angls = {}
    sidls = {}
    galaxylabel = {}
    for galaxyname in dic["星座/galaxy.json"]:
        imgls[galaxyname] = []
        angls[galaxyname] = []
        galaxylabel[galaxyname] = dic[f"星座/{galaxyname}/label.txt"]
        galaxycenter[galaxyname] = [0,0]
        scaled = [[int(stardat["pos"][0]/INITIAL_SCRSIZE[0]*screensize[0]),int(stardat["pos"][1]/INITIAL_SCRSIZE[1]*screensize[1]),stardat["star"]] for stardat in dic["星座/galaxy.json"][galaxyname]]
        starcnt = 0
        for stardat in scaled:
            if stardat[2]:
                starcnt += 1
                galaxycenter[galaxyname][0] += stardat[0]
                galaxycenter[galaxyname][1] += stardat[1]
                if f"星座/{galaxyname}/{starcnt}.jpg" in dic:
                    select = cont2img(f"星座/{galaxyname}/{starcnt}.jpg",dic).convert()
                    if screensize[0] / select.get_size()[0] > screensize[1] / select.get_size()[1]:
                        key = screensize[1] / select.get_size()[1]
                    else:
                        key = screensize[0] / select.get_size()[0]
                    image = pygame.transform.smoothscale(select,[select.get_size()[0]*key,select.get_size()[1]*key])
                    imgls[galaxyname].append({"image":image,"pos":stardat[:2],"type":randint(0,2),"rotate":randint(0,1)*2-1})
                    angls[galaxyname].append(randint(0,359))
                else:
                    imgls[galaxyname].append({"image":None,"pos":stardat[:2],"type":3,"rotate":0})
                    angls[galaxyname].append(0)
        galaxycenter[galaxyname][0] /= starcnt
        galaxycenter[galaxyname][1] /= starcnt
        sidls[galaxyname] = [stardat[:2] for stardat in scaled]
screen = pygame.display.set_mode([0,0],pygame.DOUBLEBUF|pygame.HWSURFACE|pygame.FULLSCREEN,8)
# screen = pygame.display.set_mode([1024,768])
pygame.event.set_allowed([pygame.KEYDOWN,pygame.KEYUP,pygame.MOUSEBUTTONDOWN])
screensize = screen.get_size()
keepgoing = True
first = True
alpha = 0
deltaalpha = ALPHA_DACAY
with open("logo.pdb","rb") as file:
    temp = pload(file)
logo2 = cont2img("logo2.png",temp)
logo = cont2img("logo.png",temp)
clock = pygame.time.Clock()
initd = Thread(target=init)
logo2loc = [(screensize[0]-logo2.get_size()[0])/2,(screensize[1]+logo.get_size()[1])/2]
logoloc = [(screensize[0]-logo.get_size()[0])/2,(screensize[1]-logo.get_size()[1])/2]
while True:
    screen.fill(BG_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    if alpha >= 255 - ALPHA_DACAY + 1:
        if first:
            deltaalpha = 0
            initd.start()
            first = False
        if not initd.is_alive():
            deltaalpha = -ALPHA_DACAY
            while alpha > ALPHA_DACAY - 1:
                screen.fill(BG_COLOR)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                alpha += deltaalpha
                logo.set_alpha(alpha)
                logo2.set_alpha(alpha)
                screen.blit(logo,logoloc)
                screen.blit(logo2,logo2loc)
                pygame.display.update()
                clock.tick(TICK_SPEED)
            break
    alpha += deltaalpha
    logo.set_alpha(alpha)
    logo2.set_alpha(alpha)
    screen.blit(logo,logoloc)
    screen.blit(logo2,logo2loc)
    pygame.display.update()
    clock.tick(TICK_SPEED)
del init,first,alpha,deltaalpha,logo,initd,logoloc