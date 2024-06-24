import cv2
import os

def detect_bottles(imgNum):
    # Bild einlesen
    path = os.path.join("/home/pi/LagerDetectV2", f"data/img{imgNum}.jpg")
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #blur = cv2.GaussianBlur(gray,(5,5),0)
    #ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # Bildvorverarbeitung
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    #blurred = gray
    edges = cv2.Canny(blurred, 50, 200)

    # Konturen finden
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Flaschen erkennen und markieren
    count = 0
    for contour in contours:
        # Eine einfache Annahme: Flaschen sind kreisförmig
        if len(contour) >= 5 and len(contour) <= 20:
            ellipse = cv2.fitEllipse(contour)
            cv2.ellipse(image, ellipse, (0, 255, 0), 2)
            count += 1
    cv2.imwrite(path, image)

    # Ergebnis anzeigen
    return count

if __name__ == "__main__":
    import getImages
    getImages.getImages()
    for i in range(12):
        detect_bottles(i+1)