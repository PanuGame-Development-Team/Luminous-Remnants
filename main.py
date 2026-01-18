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
    if not mouse.showing:
        speed += leftbuttondown
        speed -= rightbuttondown
    speed = round(speed * SPEED_DACAY,5)
    screen.fill(BG_COLOR)
    galaxy.update(screen,speed,mouse,mouse.alpha)
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
            mouse.click()
    draw()
pygame.quit()
for filename in os.listdir("temp"):
    os.remove("temp/" + filename)
os.rmdir("temp")