import pickle,json
from settings import *
import pygame
pygame.init()
with open("logo.pdb","wb") as file:
    dic = {"logo.png":open("resources/logo.png","rb").read(),
           "logo2.png":open("resources/logo2.png","rb").read()}
    pickle.dump(dic,file)
with open("main.pdb","wb") as file:
    dic = {"VERSION":CONSTANTS.PACKVER}
    print("正在打包:  " + "font.ttf")
    dic["font.ttf"] = open("resources/font.ttf","rb").read()
    print("正在打包:  " + "bg.ogg")
    dic["bg.ogg"] = open("resources/bg.ogg","rb").read()
    print("正在打包:  " + "bg2.ogg")
    dic["bg2.ogg"] = open("resources/bg2.ogg","rb").read()
    with open("resources/星座/galaxy.json",encoding="UTF-8") as f:
        print("正在打包:  " + "星座/galaxy.json")
        dic["星座/galaxy.json"] = json.loads(f.read())
    for galaxyname in dic["星座/galaxy.json"]:
        starcnt = 0
        for stardat in dic["星座/galaxy.json"][galaxyname]:
            if stardat["star"]:
                starcnt += 1
                try:
                    dic[f"星座/{galaxyname}/{starcnt}.jpg"] = open(f"resources/星座/{galaxyname}/{starcnt}.jpg","rb").read()
                    print("打包完成:  " + f"星座/{galaxyname}/{starcnt}.jpg")
                except:
                    pass
        try:
            dic[f"星座/{galaxyname}/label.txt"] = open(f"resources/星座/{galaxyname}/label.txt",encoding="UTF-8").read().strip("\n")
            print(f"星座'{galaxyname}'的标签设定成功")
        except:
            dic[f"星座/{galaxyname}/label.txt"] = ""
    pickle.dump(dic,file)
