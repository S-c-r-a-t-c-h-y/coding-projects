# CHAPTER 7 : COLOR DETECTION

import cv2
import numpy as np
from useful_functions import stack_images

def empty(a):
    pass

path = "Ressources/lambo.png"
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", (640, 240))

cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 19, 179, empty)
cv2.createTrackbar("Saturation Min", "TrackBars", 110, 255, empty)
cv2.createTrackbar("Saturation Max", "TrackBars", 240, 255, empty)
cv2.createTrackbar("Value Min", "TrackBars", 153, 255, empty)
cv2.createTrackbar("Value Max", "TrackBars", 255, 255, empty)

while True:
    img = cv2.imread(path)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Saturation Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Saturation Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Value Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Value Max", "TrackBars")
    
    # print(h_min, h_max, s_min, s_max, v_min, v_max)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(img_hsv, lower, upper)
    img_result = cv2.bitwise_and(img, img, mask=mask)

    img_stack = stack_images(0.5, ([img, img_hsv], [mask, img_result]))

    cv2.imshow("Images", img_stack)
    cv2.waitKey(1)