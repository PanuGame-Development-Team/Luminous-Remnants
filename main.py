import pygame
import os,sys
from uuid import uuid4
from settings import *
from time import time as currenttime
from init import *
calc_distance = lambda x1,y1,x2,y2:(x1 - x2) ** 2 + (y1 - y2) ** 2
def get_selected(mouse):
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
def draw():
    global speed,mouse,select,in_screen,screen,imgls,sidls,clock
    starttime = currenttime()
    speed += leftbuttondown
    speed -= rightbuttondown
    speed = round(speed * SPEED_DACAY,5)
    mouse = pygame.mouse.get_pos()
    select,ind = get_selected(mouse)
    if alpha != 255:# not showing or
        screen.fill(BG_COLOR)
        for galaxyname in imgls:
            for j in sidls[galaxyname]:
                j[0] += speed
            galaxycenter[galaxyname][0] += speed
            dist = (mouse[0] - galaxycenter[galaxyname][0])**2 + (mouse[1] - galaxycenter[galaxyname][1])**2
            linecolor = [(i[0] - i[1]) * (LINE_SHOW_FACTOR - alpha) / LINE_SHOW_FACTOR * max(VISIBLE_DISTANCE**2-dist,0)/VISIBLE_DISTANCE**2 + i[1] for i in zip(LINE_COLOR,BG_COLOR)]
            fontcolor = [(i[0] - i[1]) * (LABEL_SHOW_FACTOR - alpha) / LABEL_SHOW_FACTOR * max(VISIBLE_DISTANCE**2-dist,0)/VISIBLE_DISTANCE**2 + i[1] for i in zip(LABEL_COLOR,BG_COLOR)]
            galnamesurf = labelfont.render(galaxyname,1,fontcolor)
            if not galaxylabel[galaxyname]:
                screen.blit(galnamesurf,[galaxycenter[galaxyname][0] - (galnamesurf.get_width()/2),galaxycenter[galaxyname][1] - (galnamesurf.get_height()/2)])
            else:
                labelsurf = labelfont.render(galaxylabel[galaxyname],1,fontcolor)
                screen.blit(galnamesurf,[galaxycenter[galaxyname][0] - (galnamesurf.get_width()/2),galaxycenter[galaxyname][1] - (galnamesurf.get_height()/2) - LABEL_DISPSIZE / 2])
                screen.blit(labelsurf,[galaxycenter[galaxyname][0] - (labelsurf.get_width()/2),galaxycenter[galaxyname][1] - (labelsurf.get_height()/2) + LABEL_DISPSIZE / 2])
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
                if galaxycenter[galaxyname][0] > screensize[0]:
                    galaxycenter[galaxyname][0] -= screensize[0] * 2
                elif galaxycenter[galaxyname][0] < 0:
                    galaxycenter[galaxyname][0] += screensize[0] * 2
    if showing and alpha != 255:
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
speed = 0
leftbuttondown = rightbuttondown = False
showing = False
select = False
showing = False
alpha = 0
bgm.play(-1)
while keepgoing:
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
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                keepgoing = False
                                alpha = ALPHA_DACAY
                    draw()
                    alpha -= ALPHA_DACAY
                alpha = 0
                showing = False
    draw()
pygame.quit()
for filename in os.listdir("temp"):
    os.remove("temp/" + filename)
os.rmdir("temp")