import pygame
import os,sys
from threading import Thread
from random import choice,randint
from pickle import load as pload
from uuid import uuid4
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
            if imgls[i][j][3] != 3 and calc_distance(*imgls[i][j][1:3],*mouse) < nearest_distance:
                nearest = imgls[i][j][0]
                nearest_distance = calc_distance(*imgls[i][j][1:3],*mouse)
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
    global imgls,angls,sidls,bgm,star,gal_pla,gpang
    with open("main.pdb","rb") as file:
        tmp = pload(file)
    star4 = cont2img("4.png",tmp)
    star5 = cont2img("5.png",tmp)
    star6 = cont2img("6.png",tmp)
    starlock = cont2img("lock.png",tmp)
    star = [star4,star5,star6,starlock]
    gal_pla = [[cont2img("星系2.png",tmp),746,350,-0.1]]
    gpang = [randint(0,359)]
    bgm = pygame.mixer.Sound(savdat("ogg",tmp["bg.ogg"]))
    imgls = {}
    angls = {}
    sidls = {}
    cont = tmp["星座/星座.txt"]
    lines = cont.strip("\n").split("\n")
    screensize = screen.get_size()
    for i in lines:
        name = i.strip(" ").split(" ")[0]
        imgls[name] = []
        angls[name] = []
        temp = [j.split(",") for j in i.strip(" ").split(" ")[1:]]
        temp = [[int(int(j[0])/1536*screensize[0]),int(int(j[1])/864*screensize[1]),int(j[2])] for j in temp]
        k = 0
        for j in temp:
            if j[2] == 1:
                k += 1
                if f"星座/{name}/{k}.jpg" in tmp:
                    select = cont2img(f"星座/{name}/{k}.jpg",tmp).convert()
                    if screen.get_size()[0] / select.get_size()[0] > screen.get_size()[1] / select.get_size()[1]:
                        key = screen.get_size()[1] / select.get_size()[1]
                    else:
                        key = screen.get_size()[0] / select.get_size()[0]
                    image = pygame.transform.smoothscale(select,[select.get_size()[0]*key,select.get_size()[1]*key])
                    imgls[name].append([image,j[0],j[1],randint(0,2),randint(0,1)*2-1])
                    angls[name].append(randint(0,359))
                else:
                    imgls[name].append([None,j[0],j[1],3,0])
                    angls[name].append(0)
        sidls[name] = [j[:-1] for j in temp]
def draw():
    global speed,mouse,select,gal_pla,in_screen,gpang,screen,imgls,sidls,clock
    speed += kdl
    speed -= kdr
    speed = round(speed*0.95,5)
    mouse = pygame.mouse.get_pos()
    s = screen.convert_alpha()
    for i in range(len(gal_pla)):
        gal_pla[i][1] += speed / 10
        in_screen = False
        img = pygame.transform.rotate(gal_pla[i][0],gpang[i])
        gpang[i] = (gpang[i] + gal_pla[i][3]) % 360
        img.set_alpha(255 - alpha)
        rect = img.get_rect()
        rect.center = gal_pla[i][1:3]
        if rect.centerx + img.get_width() / 2 > 0 and rect.centerx - img.get_width() / 2 < screen.get_size()[0]:
            in_screen = True
        if in_screen:
            s.blit(img,rect)
        else:
            if gal_pla[i][1] > screen.get_size()[0]:
                gal_pla[i][1] -= screen.get_size()[0] * 2
            elif gal_pla[i][1] < 0:
                gal_pla[i][1] += screen.get_size()[0] * 2
                
    select,ind = get_selected(i,mouse)
    for i in imgls:
        for j in sidls[i]:
            j[0] += speed
        pygame.draw.aalines(s,[255,255,255,255 - alpha],False,sidls[i])
        in_screen = False
        for j in range(len(imgls[i])):
            img = pygame.transform.rotate(star[imgls[i][j][3]],angls[i][j])
            if i == ind[0] and j == ind[1]:
                img = pygame.transform.scale2x(img)
            angls[i][j] = (angls[i][j] + imgls[i][j][4]) % 360
            rect = img.get_rect()
            imgls[i][j][1] += speed
            if imgls[i][j][1] > 0 and imgls[i][j][1] < screen.get_size()[0]:
                in_screen = True
            rect.center = imgls[i][j][1:3]
            img.set_alpha(255 - alpha)
            s.blit(img,rect)
        if not in_screen:
            for j in imgls[i]:
                if j[1] > screen.get_size()[0]:
                    j[1] -= screen.get_size()[0] * 2
                elif j[1] < 0:
                    j[1] += screen.get_size()[0] * 2
            for j in sidls[i]:
                if j[0] > screen.get_size()[0]:
                    j[0] -= screen.get_size()[0] * 2
                elif j[0] < 0:
                    j[0] += screen.get_size()[0] * 2
    if showing:
        image.set_alpha(alpha)
        s.blit(image,loc)
    screen.blit(s,[0,0])
    pygame.display.update()
    clock.tick(60)




screen = pygame.display.set_mode([0,0],pygame.DOUBLEBUF|pygame.HWSURFACE|pygame.FULLSCREEN,8)
pygame.event.set_allowed([pygame.KEYDOWN,pygame.KEYUP,pygame.MOUSEBUTTONDOWN])
keepgoing = True
first = True
alpha = 0
asp = 3
with open("logo.pdb","rb") as file:
    temp = pload(file)
logo2 = cont2img("logo2.png",temp)
logo = cont2img("logo.png",temp)
clock = pygame.time.Clock()
initd = Thread(target=init)
logo2loc = [(screen.get_size()[0]-logo2.get_size()[0])/2,(screen.get_size()[1]+logo.get_size()[1])/2]
logoloc = [(screen.get_size()[0]-logo.get_size()[0])/2,(screen.get_size()[1]-logo.get_size()[1])/2]
while True:
    screen.fill([0,0,30])
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    if alpha >= 253:
        if first:
            asp = 0
            initd.start()
            first = False
        if not initd.is_alive():
            asp = -3
            while alpha > 2:
                screen.fill([0,0,30])
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                alpha += asp
                logo.set_alpha(alpha)
                logo2.set_alpha(alpha)
                screen.blit(logo,logoloc)
                screen.blit(logo2,logo2loc)
                pygame.display.update()
                clock.tick(60)
            break
    alpha += asp
    logo.set_alpha(alpha)
    logo2.set_alpha(alpha)
    screen.blit(logo,logoloc)
    screen.blit(logo2,logo2loc)
    pygame.display.update()
    clock.tick(60)
del init,first,alpha,asp,logo,initd,logoloc




speed = 0
kdl = kdr = False
showing = False
select = False
showing = False
alpha = 0
bgm.play(-1)
while keepgoing:
    screen.fill([0,0,30])
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                keepgoing = False
            elif event.key == pygame.K_LEFT:
                kdl = True
            elif event.key == pygame.K_RIGHT:
                kdr = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                kdl = False
            elif event.key == pygame.K_RIGHT:
                kdr = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if select:
                showing = True
                loc = [0,0]
                loc[0] = abs(screen.get_size()[0] - select.get_size()[0]) / 2
                loc[1] = abs(screen.get_size()[1] - select.get_size()[1]) / 2
                image = pygame.transform.smoothscale(select,select.get_size())
            if showing:
                kg = True
                kdl = kdr = False
                alpha = 0
                while kg:
                    screen.fill([0,0,30])
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                kg = False
                                keepgoing = False
                                alpha = -3
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            kg = False
                    if alpha < 253:
                        alpha += 3
                    else:
                        alpha = 255
                    draw()
                while alpha > 0:
                    screen.fill([0,0,30])
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                keepgoing = False
                                alpha = 3
                    draw()
                    alpha -= 3
                alpha = 0
                showing = False
                screen.fill([0,0,30])
    draw()
pygame.quit()
