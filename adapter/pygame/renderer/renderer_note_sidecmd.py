from usecase.usecase import UseCase
from adapter.settings import NOTE
from adapter.pygame.renderer.uimath import *
import os
import pygame
class SideCMD(UseCase.Renderer):
    cache = {}          # Key: name,bold,italic
    def __init__(self,display:pygame.surface.Surface,scrsize,font:pygame.font.Font,order=NOTE.ORDER):
        self.display = display
        self.scrsize = scrsize
        self.font = font
        self.order = order
    def render(self,object:UseCase.Note):
        if not NOTE.ENABLE:
            return
        messages = object.get_messages()
        if NOTE.CMD and len(messages) > len(self.order):
            os.system("cls" if os.name == "nt" else "clear")
        i = 0
        for title in messages:
            if i < len(self.order):
                surf = self.render_one(title,bold=True)
                h = surf.get_height()
                ls = [surf]
                for message in messages[title]:
                    surf = self.render_one(message)
                    h += surf.get_height()
                    ls.append(surf)
                self.to_display(ls,h,self.order[i])
                i += 1
            else:
                self.to_console([title] + messages[title])
    def render_one(self,text:str,color=NOTE.DEFAULT_COLOR,bold:bool=False,italic:bool=False) -> pygame.surface.Surface:
        if not (text,tuple(color),bold,italic) in self.cache:
            self.font.set_bold(bold)
            self.font.set_italic(italic)
            if len(self.cache) >= NOTE.CACHE_KEY_SIZE:
                self.cache.clear()
            self.cache[text,tuple(color),bold,italic] = self.font.render(text,NOTE.ANTIALIAS,color)
        return self.cache[text,tuple(color),bold,italic]
    def to_display(self,ls:list[pygame.surface.Surface],h:int,anchor:str=""):
        if "s" in anchor:
            y = self.scrsize[1] - h
        else:
            y = 0
        if "e" in anchor:
            l = False
        else:
            l = True
        for surf in ls:
            self.display.blit(surf,[0 if l else self.scrsize[0] - surf.get_width(),y])
            y += surf.get_height()
    def to_console(self,messages:list[str]):
        print("NAMESPACE: ",messages.pop(0))
        print(*messages,sep="\n",end="\n---END---\n\n")