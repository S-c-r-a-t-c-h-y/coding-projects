# CHAPTER 9 : FACE DETECTION

import cv2
import numpy as np
from useful_functions import *

face_cascade = cv2.CascadeClassifier("Ressources/haarcascades/haarcascade_frontalface_default.xml")

# img = cv2.imread("Ressources/sample_image.png")
# img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# faces = face_cascade.detectMultiScale(img_gray, 1.1, 4)
# for (x, y, w, h) in faces:
#     cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

# cv2.imshow("Image", img)
# # cv2.imshow("Grayscale", img_gray)
# cv2.waitKey(0)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 100)

while 1:
    success, img = cap.read()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(img_gray, 1.1, 4)
    for (x, y, w, h) in faces:
        # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        img_cropped = img[y: y+h, x:x+w]
        cv2.imshow("Video", img_cropped)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break