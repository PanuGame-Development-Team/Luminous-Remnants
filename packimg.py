import pickle,json
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
    with open("星座/galaxy.json",encoding="UTF-8") as f:
        print("正在打包:  " + "星座/galaxy.json")
        dic["星座/galaxy.json"] = json.loads(f.read())
    for galaxyname in dic["星座/galaxy.json"]:
        starcnt = 0
        for stardat in dic["星座/galaxy.json"][galaxyname]:
            if stardat["star"]:
                starcnt += 1
                try:
                    dic[f"星座/{galaxyname}/{starcnt}.jpg"] = open(f"星座/{galaxyname}/{starcnt}.jpg","rb").read()
                    print("打包完成:  " + f"星座/{galaxyname}/{starcnt}.jpg")
                except:
                    pass
        try:
            dic[f"星座/{galaxyname}/label.txt"] = open(f"星座/{galaxyname}/label.txt",encoding="UTF-8").read()
            print(f"星座'{galaxyname}'的标签设定成功")
        except:
            dic[f"星座/{galaxyname}/label.txt"] = ""
    pickle.dump(dic,file)
