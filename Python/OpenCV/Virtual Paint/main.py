# PROJECT 1 : VIRTUAL PAINT

import cv2
import numpy as np

FRAME_WIDTH, FRAME_HEIGHT = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, FRAME_WIDTH)
cap.set(4, FRAME_HEIGHT)
cap.set(10, 150)

my_colors = [
    
]

def find_color(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(img_hsv, lower, upper)
    cv2.imshow("img", mask)

while True:
    success, img = cap.read()
    
    
    
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

