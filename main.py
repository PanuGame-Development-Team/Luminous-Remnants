import pygame
import os,sys
from threading import Thread
from random import randint
from pickle import load as pload
from uuid import uuid4
from settings import *
from time import time as currenttime
if not os.path.isdir("temp"):
    os.mkdir("temp")
pygame.init()
calc_distance = lambda x1,y1,x2,y2:(x1 - x2) ** 2 + (y1 - y2) ** 2
def get_selected(i,mouse):
    nearest = None
    nearest_distance = 1e9
    nearest_id = [None,None]
    for i in imgls:
        for j in range(len(imgls[i])):
            if imgls[i][j]["type"] != 3 and calc_distance(*imgls[i][j]["pos"],*mouse) < nearest_distance:
                nearest = imgls[i][j]["image"]
                nearest_distance = calc_distance(*imgls[i][j]["pos"],*mouse)
                nearest_id = [i,j]
    if nearest_distance > 100:
        return None,[None,None]
    return nearest,nearest_id
def savdat(name,dat):
    filename = "temp/" + uuid4().hex + "." + name.split(".")[-1]
    with open(filename,"wb") as file:
        file.write(dat)
    return filename
def cont2img(index:str,dic:dict):
    filename = savdat(index,dic[index])
    return pygame.image.load(filename).convert_alpha()
def init():
    global imgls,angls,sidls,bgm,star,galaxypos,galaxyangls,galaxycenter,starrotated
    with open("main.pdb","rb") as file:
        dic = pload(file)
    star4 = cont2img("4.png",dic)
    star5 = cont2img("5.png",dic)
    star6 = cont2img("6.png",dic)
    starlock = cont2img("lock.png",dic)
    star = [star4,star5,star6,starlock]
    starrotated = [[],[],[],[starlock]]
    for angle in range(360):
        starrotated[0].append(pygame.transform.rotate(star4,angle))
        starrotated[1].append(pygame.transform.rotate(star5,angle))
        starrotated[2].append(pygame.transform.rotate(star6,angle))
    galaxypos = [[cont2img("星系2.png",dic)] + GAL_SPEED["星系2"]]
    galaxyangls = [randint(0,359)]
    bgm = pygame.mixer.Sound(savdat("ogg",dic["bg.ogg"]))
    galaxycenter = {}
    imgls = {}
    angls = {}
    sidls = {}
    for galaxyname in dic["星座/galaxy.json"]:
        imgls[galaxyname] = []
        angls[galaxyname] = []
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
def draw():
    global speed,mouse,select,galaxypos,in_screen,galaxyangls,screen,imgls,sidls,clock
    starttime = currenttime()
    speed += leftbuttondown
    speed -= rightbuttondown
    speed = round(speed * SPEED_DACAY,5)
    mouse = pygame.mouse.get_pos()
    for i in range(len(galaxypos)):
        galaxypos[i][1] += speed * BG_GALAXY_SPEED
        in_screen = False
        img = pygame.transform.rotate(galaxypos[i][0],galaxyangls[i])
        galaxyangls[i] = (galaxyangls[i] + galaxypos[i][3]) % 360
        img.set_alpha(255 - alpha)
        rect = img.get_rect()
        rect.center = galaxypos[i][1:3]
        if rect.centerx + img.get_width() / 2 > 0 and rect.centerx - img.get_width() / 2 < screensize[0]:
            in_screen = True
        if in_screen:
            screen.blit(img,rect)
        else:
            if galaxypos[i][1] > screensize[0]:
                galaxypos[i][1] -= screensize[0] * 2
            elif galaxypos[i][1] < 0:
                galaxypos[i][1] += screensize[0] * 2
    select,ind = get_selected(i,mouse)
    for galaxyname in imgls:
        for j in sidls[galaxyname]:
            j[0] += speed
        linecolor = [i * (360 - alpha) / 360 for i in LINE_COLOR]
        pygame.draw.aalines(screen,linecolor,False,sidls[galaxyname])
        in_screen = False
        for j in range(len(imgls[galaxyname])):
            img = starrotated[imgls[galaxyname][j]["type"]][angls[galaxyname][j]]
            if galaxyname == ind[0] and j == ind[1]:
                img = pygame.transform.scale2x(img)
            angls[galaxyname][j] = (angls[galaxyname][j] + imgls[galaxyname][j]["rotate"]) % 360
            rect = img.get_rect()
            imgls[galaxyname][j]["pos"][0] += speed
            if imgls[galaxyname][j]["pos"][0] > 0 and imgls[galaxyname][j]["pos"][0] < screensize[0]:
                in_screen = True
            rect.center = imgls[galaxyname][j]["pos"]
            img.set_alpha(255 - alpha)
            screen.blit(img,rect)
        if not in_screen:
            for j in imgls[galaxyname]:
                if j["pos"][0] > screensize[0]:
                    j["pos"][0] -= screensize[0] * 2
                elif j["pos"][0] < 0:
                    j["pos"][0] += screensize[0] * 2
            for j in sidls[galaxyname]:
                if j[0] > screensize[0]:
                    j[0] -= screensize[0] * 2
                elif j[0] < 0:
                    j[0] += screensize[0] * 2
    if showing:
        image.set_alpha(alpha)
        screen.blit(image,loc)
    pygame.display.update()
    if PERFORMANCE_TRACK:
        endtime = currenttime()
        if endtime - starttime >= 1.5 / TICK_SPEED:
            print("Performance warning: expected %.3fms, %3fms"%(1/TICK_SPEED,endtime - starttime))
        elif endtime - starttime <= 0.4 / TICK_SPEED:
            print("Performance warning: expected %.3fms, %3fms"%(1/TICK_SPEED,endtime - starttime))
    clock.tick(TICK_SPEED)




# screen = pygame.display.set_mode([0,0],pygame.DOUBLEBUF|pygame.HWSURFACE|pygame.FULLSCREEN,8)
screen = pygame.display.set_mode([1024,768])
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




speed = 0
leftbuttondown = rightbuttondown = False
showing = False
select = False
showing = False
alpha = 0
bgm.play(-1)
while keepgoing:
    screen.fill(BG_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                keepgoing = False
            elif event.key == pygame.K_LEFT:
                leftbuttondown = True
            elif event.key == pygame.K_RIGHT:
                rightbuttondown = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                leftbuttondown = False
            elif event.key == pygame.K_RIGHT:
                rightbuttondown = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if select:
                showing = True
                loc = [0,0]
                loc[0] = abs(screensize[0] - select.get_size()[0]) / 2
                loc[1] = abs(screensize[1] - select.get_size()[1]) / 2
                image = pygame.transform.smoothscale(select,select.get_size())
            if showing:
                innerkeepgoing = True
                leftbuttondown = rightbuttondown = False
                alpha = 0
                while innerkeepgoing:
                    screen.fill(BG_COLOR)
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                innerkeepgoing = False
                                keepgoing = False
                                alpha = -ALPHA_DACAY
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            innerkeepgoing = False
                    if alpha < 255 - ALPHA_DACAY + 1:
                        alpha += ALPHA_DACAY
                    else:
                        alpha = 255
                    draw()
                while alpha > 0:
                    screen.fill(BG_COLOR)
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                keepgoing = False
                                alpha = ALPHA_DACAY
                    draw()
                    alpha -= ALPHA_DACAY
                alpha = 0
                showing = False
                screen.fill(BG_COLOR)
    draw()
pygame.quit()
