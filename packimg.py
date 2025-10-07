import pickle
import pygame
pygame.init()
# def imga2ls(img):
#     return [pygame.image.tostring(img,"RGBA"),img.get_size()]
# def img2ls(img):
#     return [pygame.image.tostring(img,"RGB"),img.get_size()]
with open("logo.pdb","wb") as file:
    dic = {"logo.png":open("logo.png","rb").read(),
           "logo2.png":open("logo2.png","rb").read()}
    pickle.dump(dic,file)
with open("main.pdb","wb") as file:
    print("正在打包:  " + "星系2.png")
    dic = {"星系2.png":open("星系2.png","rb").read()}
    print("正在打包:  " + "4.png")
    dic["4.png"] = open("4.png","rb").read()
    print("正在打包:  " + "5.png")
    dic["5.png"] = open("5.png","rb").read()
    print("正在打包:  " + "6.png")
    dic["6.png"] = open("6.png","rb").read()
    print("正在打包:  " + "lock.png")
    dic["lock.png"] = open("lock.png","rb").read()
    print("正在打包:  " + "bg.ogg")
    dic["bg.ogg"] = open("bg.ogg","rb").read()
    with open("星座/星座.txt",encoding="UTF-8") as f:
        print("正在打包:  " + "星座/星座.txt")
        dic["星座/星座.txt"] = f.read()
    lines = dic["星座/星座.txt"].strip("\n").split("\n")
    for i in lines:
        name = i.strip(" ").split(" ")[0]
        posls = [[int(k[0]),int(k[1]),int(k[2])] for k in [j.split(",") for j in i.strip(" ").split(" ")[1:]]]
        k = 0
        for j in posls:
            if j[2] == 1:
                k += 1
                print("正在打包:  " + f"星座/{name}/{k}.jpg")
                try:
                    dic[f"星座/{name}/{k}.jpg"] = open(f"星座/{name}/{k}.jpg","rb").read()
                except:
                    print(f"警告:无法读取'星座/{name}/{k}.jpg',星图将锁定这颗星")
    pickle.dump(dic,file)
