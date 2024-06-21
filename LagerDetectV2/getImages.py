import cv2
from mkPic import mkPic
import os
import subprocess
from time import sleep

def getImages():
    #path = os.path.join(os.getcwd(), "data/img.jpg")
    path = "/home/pi/LagerDetectV2/data/img.jpg"
    os.system("/home/pi/LagerDetectV2/LagerDetectV2/mkPic.sh")
    #mkPic()

    img = cv2.imread(path)

    imArr = [
        img[270:480,100:360],
        img[260:460,390:660],
        img[270:470,730:1000],
        img[300:460,1040:1260],

        img[500:650,170:400],
        img[500:660,430:660],
        img[500:650,730:960],
        img[500:650,1000:1210],

        img[660:830,200:400],
        img[670:830,440:670],
        img[680:830,730:950],
        img[660:820,950:1180]
    ]
    i = 1
    for img in imArr:
        cv2.imwrite(path.replace("img", f"img{i}"), img)
        i += 1

if __name__ == "__main__":
    getImages()