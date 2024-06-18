import cv2
import os


def mkPic():
    cap = cv2.VideoCapture(0)

    success, frame = cap.read()
    cap.release()
    #if success:
    cv2.imwrite(os.path.join(os.getcwd(), "data/img.jpg"), frame)
    #else:
    #    raise Exception("Error while taking picture.")

if __name__ == "__main__":
    mkPic()