from usecase.usecase import UseCase
from adapter.settings import *
from ca import *
from os.path import isfile
from hashlib import md5
from pickle import load
from random import random,choice
import pygame
def savdat(name,dat,hashfunc=md5):
    filename = "temp/" + hashfunc(name.encode()).hexdigest() + "." + name.split(".")[-1]
    with open(filename,"wb") as file:
        file.write(dat)
    return filename
def cont2img(index:str,dic:dict) -> pygame.surface.Surface:
    filename = savdat(index,dic[index])
    return pygame.image.load(filename).convert_alpha()
class Pickle(UseCase.DataProvider):
    def __init__(self,screensize,filename="main.lrg"):
        super().__init__()
        self.screensize = screensize
        self.filename = filename
    res = {}
    startot = 0
    path = {}
    def load_logo(self):
        if not isfile("logo.dat"):
            raise FileNotFoundError("logo.dat")
        with open("logo.dat","rb") as file:
            dic = load(file)
        self.rman = UseCase.Entity.ResourceManager()
        logo = self.rman.register(cont2img("logo.png",dic))
        logo2 = self.rman.register(cont2img("logo2.png",dic))
        return logo,logo2
    def load_data(self):
        if not isfile(self.filename):
            raise FileNotFoundError(self.filename)
        with open(self.filename,"rb") as file:
            dic = self.dic = load(file)
        if dic.get("VERSION") == "1.2-rev1":
            self.load_1_2_rev1(dic)
            return
        if dic.get("VERSION") != CONSTANTS.PACKVER:
            raise RuntimeError("Package version incompatible. Expected %s, received %s"%(CONSTANTS.PACKVER,dic.get("VERSION")))
        self.load(dic)
    def load(self,dic):
        self.path["namefont"] = savdat("ttf",dic["font.ttf"])
        self.res["namefont"] = self.datrman.register(pygame.font.Font(self.path["namefont"],GALAXY.LABEL_DISPSIZE))
        self.path["bgm"] = []
        self.res["bgm"] = []
        for i in dic["bg.ogg"]:
            self.path["bgm"].append(savdat("ogg",i))
            self.res["bgm"].append(self.datrman.register(pygame.mixer.Sound(self.path["bgm"][-1])))
        self.res["galaxy"] = {}
        for galaxyname in dic["星座/galaxy.json"]:
            stars = []
            formatted = [[UseCase.Entity.Pos(*stardat["pos"],*GENERAL.INITIAL_SCRSIZE).scale(*self.screensize),stardat["star"]] for stardat in dic["星座/galaxy.json"][galaxyname][:-1]]
            starcnt = 0
            for stardat in formatted:
                if stardat[1]:
                    starcnt += 1
                    if f"星座/{galaxyname}/{starcnt}.jpg" in dic:
                        img = cont2img(f"星座/{galaxyname}/{starcnt}.jpg",dic)
                        pic = UseCase.Picture(self.datrman.register(pygame.transform.smoothscale_by(img,min(self.screensize[0] / img.get_width(),self.screensize[1] / img.get_height())).convert()))
                        stars.append(UseCase.Star(random()*360,choice([STAR.ROTATION,-STAR.ROTATION]),stardat[0],False,pic))
                    else:
                        stars.append(UseCase.Star(0,0,stardat[0],True,None))
            lines = [[formatted[i[0]][0],formatted[i[1]][0]] for i in dic["星座/galaxy.json"][galaxyname][-1]]
            self.res["galaxy"][galaxyname] = self.datrman.register(UseCase.Galaxy(galaxyname,dic[f"星座/{galaxyname}/label.txt"],stars,lines))
    def load_1_2_rev1(self,dic):
        self.path["namefont"] = savdat("ttf",dic["font.ttf"])
        self.res["namefont"] = self.datrman.register(pygame.font.Font(self.path["namefont"],GALAXY.LABEL_DISPSIZE))
        self.path["bgm"] = []
        self.res["bgm"] = []
        for i in dic["bg.ogg"]:
            self.path["bgm"].append(savdat("ogg",i))
            self.res["bgm"].append(self.datrman.register(pygame.mixer.Sound(self.path["bgm"][-1])))
        self.res["galaxy"] = {}
        for galaxyname in dic["星座/galaxy.json"]:
            stars = []
            formatted = [[UseCase.Entity.Pos(*stardat["pos"],*GENERAL.INITIAL_SCRSIZE).scale(*self.screensize),stardat["star"]] for stardat in dic["星座/galaxy.json"][galaxyname]]
            starcnt = 0
            for stardat in formatted:
                if stardat[1]:
                    starcnt += 1
                    if f"星座/{galaxyname}/{starcnt}.jpg" in dic:
                        img = cont2img(f"星座/{galaxyname}/{starcnt}.jpg",dic)
                        pic = UseCase.Picture(self.datrman.register(pygame.transform.smoothscale_by(img,min(self.screensize[0] / img.get_width(),self.screensize[1] / img.get_height())).convert()))
                        stars.append(UseCase.Star(random()*360,choice([STAR.ROTATION,-STAR.ROTATION]),stardat[0],False,pic))
                    else:
                        stars.append(UseCase.Star(0,0,stardat[0],True,None))
            lines = [[formatted[i][0],formatted[i+1][0]] for i in range(len(formatted) - 1)]
            self.res["galaxy"][galaxyname] = self.datrman.register(UseCase.Galaxy(galaxyname,dic[f"星座/{galaxyname}/label.txt"],stars,lines))
    def tick(self):
        return self.datrman
    def resource(self,name:str):
        return self.res.get(name)