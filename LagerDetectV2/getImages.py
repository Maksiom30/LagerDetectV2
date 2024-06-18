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
        img[240:460,100:390],
        img[240:460,390:660],
        img[240:460,700:1020],
        img[240:460,1000:],

        img[450:650,150:400],
        img[450:650,390:660],
        img[450:650,700:1020],
        img[450:650,1000:],

        img[630:830,200:400],
        img[640:830,440:670],
        img[630:830,700:960],
        img[630:830,950:1200]
    ]
    i = 1
    for img in imArr:
        cv2.imwrite(path.replace("img", f"img{i}"), img)
        i += 1

if __name__ == "__main__":
    getImages()