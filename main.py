import pygame
from init import *
import os
from settings import *
from sprites.mouse import Mouse
from sprites.meteor import Meteor
from lib import *
if AUTOPLAY.ENABLE:
    from time import time
    t0 = time()
    dest = [0,0]
speed = 0
leftbuttondown = rightbuttondown = False
showing = False
select = False
showing = False
bgm.play(-1)
mouse = Mouse()
meteor = pygame.sprite.Group()
while keepgoing:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                keepgoing = False
            elif event.key == pygame.K_LEFT:
                leftbuttondown = True
            elif event.key == pygame.K_RIGHT:
                rightbuttondown = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                leftbuttondown = False
            elif event.key == pygame.K_RIGHT:
                rightbuttondown = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not AUTOPLAY.ENABLE:
                mouse.click()
    if not AUTOPLAY.ENABLE:
        if not mouse.showing:
            speed += leftbuttondown
            speed -= rightbuttondown
        speed = round(speed * GENERAL.SPEED_DACAY,5)
    else:
        speed = scroller.speed()
        if time() - t0 > sched[0][0]:
            if sched[0][1] == "click":
                mouse.click()
            elif sched[0][1] == "quit":
                keepgoing = False
            elif sched[0][1] == "move":
                mouse.autoplay.dest = galaxy.sprites()[dest[0]].stars.sprites()[dest[1]].pos
                mouse.autoplay.outset = mouse.pos
                mouse.autoplay.moving = True
                find_next(dest,galaxy)
            elif sched[0][1] == "checkbg":
                gal = galaxy.sprites()[dest[0]]
                if gal.right > screensize[0] * (1 - AUTOPLAY.SCROLL_BG_FACTOR):
                    scroller.scroll(gal.left - screensize[0] * AUTOPLAY.SCROLL_BG_FACTOR)
                if gal.right < 0:
                    scroller.scroll(gal.left - screensize[0] * (AUTOPLAY.SCROLL_BG_FACTOR - 2))
            sched.pop(0)
    screen.fill(GENERAL.BG_COLOR)
    galaxy.update(screen,speed,mouse,mouse.alpha)
    meteor.update(screen,speed,mouse.alpha)
    mouse.update(screen,pygame.mouse.get_pos())
    pygame.display.update()
    clock.tick(CONSTANTS.TICK_SPEED)
pygame.quit()
for filename in os.listdir("temp"):
    os.remove("temp/" + filename)
os.rmdir("temp")