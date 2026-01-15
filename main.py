import pygame
from init import *
import os
from settings import *
from time import time as currenttime
from sprites.mouse import Mouse
from lib import *
# def get_selected():
#     nearest = None
#     nearest_distance = 1e9
#     nearest_id = [None,None]
#     for i in imgls:
#         for j in range(len(imgls[i])):
#             if imgls[i][j]["type"] != 3 and calc_distance_sq(*imgls[i][j]["pos"],*mouse.pos) < nearest_distance:
#                 nearest = imgls[i][j]["image"]
#                 nearest_distance = calc_distance_sq(*imgls[i][j]["pos"],*mouse.pos)
#                 nearest_id = [i,j]
#     if nearest_distance > 100:
#         return None,[None,None]
#     return nearest,nearest_id
def draw():
    global speed,select,screen,clock
    starttime = currenttime()
    speed += leftbuttondown
    speed -= rightbuttondown
    speed = round(speed * SPEED_DACAY,5)
    # select,ind = get_selected()
    screen.fill(BG_COLOR)
    galaxy.update(screen,speed,mouse.pos,alpha)
    if showing:
        image.set_alpha(alpha)
        screen.blit(image,loc)
    mouse.update(screen,pygame.mouse.get_pos())
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
mouse = Mouse()
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
            mouse.rotating = True
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