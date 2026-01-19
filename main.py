import pygame
from init import *
import os
from settings import *
from time import time as currenttime
from sprites.mouse import Mouse
from lib import *
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
    if not mouse.showing:
        speed += leftbuttondown
        speed -= rightbuttondown
    speed = round(speed * GENERAL.SPEED_DACAY,5)
    screen.fill(GENERAL.BG_COLOR)
    galaxy.update(screen,speed,mouse,mouse.alpha)
    mouse.update(screen,pygame.mouse.get_pos())
    pygame.display.update()
    clock.tick(CONSTANTS.TICK_SPEED)
pygame.quit()
for filename in os.listdir("temp"):
    os.remove("temp/" + filename)
os.rmdir("temp")