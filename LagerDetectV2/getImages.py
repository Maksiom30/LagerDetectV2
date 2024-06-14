import cv2
from mkPic import mkPic
import os

def getImages():
    path = os.path.join(os.getcwd(), "data/img.jpg")
    mkPic()

    img = cv2.imread(path)

    img1 = img[240:330,140:250]
    cv2.imwrite(path.replace("img", "img1"), img1)

    img2 = img[150:220,150:255]
    cv2.imwrite(path.replace("img", "img2"),img2)

    img3 = img[240:330,310:420]
    cv2.imwrite(path.replace("img", "img3"),img3)

if __name__ == "__main__":
    getImages()