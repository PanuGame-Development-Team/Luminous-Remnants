from usecase.usecase import UseCase
from adapter.pygame.renderer.uimath import centrialize,color_adapt
from adapter.pygame.renderer.renderer_note_sidecmd import SideCMD
from settings import *
import pygame
def loadall(screen:pygame.surface.Surface,dataprovider:UseCase.DataProvider,clock:pygame.time.Clock,footnotes:UseCase.Note) -> bool:
    logo,logo2 = dataprovider.load_logo()
    footnotefont = pygame.font.SysFont(INIT.DEFAULT_FONT,INIT.FOOTNOTE_FONT_SIZE)
    screensize = screen.get_size()
    nr = SideCMD(screen,screensize,footnotefont,["se"])
    logoloc = centrialize(screensize[0]/2,screensize[1]/2,logo.get().get_width(),0,0,-logo.get().get_height()/2)
    logo2loc = centrialize(screensize[0]/2,screensize[1]/2,logo2.get().get_width(),0,0,logo.get().get_height()/2)
    deltaalpha = PICTURE.ALPHA_DECAY
    alpha = 0
    while True:
        screen.fill(GENERAL.BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
        alpha += deltaalpha
        if alpha > 255:
            alpha = 255
            deltaalpha = 0
            dataprovider.load_data()
        if alpha < 0:
            break
        nr.render(footnotes)
        logo.get().set_alpha(alpha)
        logo2.get().set_alpha(alpha)
        screen.blit(logo.get(),logoloc)
        screen.blit(logo2.get(),logo2loc)
        pygame.display.update()
        if deltaalpha == 0 and dataprovider.tick():
            deltaalpha = -PICTURE.ALPHA_DECAY
        clock.tick(CONSTANTS.TICK_SPEED)
    return True