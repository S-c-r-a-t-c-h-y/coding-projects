# PROJECT 2 : DOCUMENT SCANNER

import cv2
import numpy as np
import os, sys
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from useful_functions import stack_images

FRAME_WIDTH = 720//2
FRAME_HEIGHT = 1400//2

url = "http://192.168.1.46:8080//shot.jpg"

blank_img = np.zeros((FRAME_WIDTH, FRAME_HEIGHT), np.uint8)

def get_img_treshold(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (7, 7), 1)
    img_canny = cv2.Canny(img_blur, 75, 200)
    # cv2.imshow("Canny", img_canny)
    kernel = np.ones((5, 5))
    img_dialation = cv2.dilate(img_canny, kernel, iterations=2)
    img_eroded = cv2.erode(img_dialation, kernel, iterations=1)
    return img_eroded
    
def get_contours(img, area_treshold=5000, points_treshold=0.02):
    biggest = None
    biggest_approx = np.array([])
    max_area = 0
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > area_treshold:
            # cv2.drawContours(img_contour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, points_treshold*peri, True)
            if area > max_area and len(approx) == 4:
                max_area = area
                biggest = cnt
                biggest_approx = approx
    cv2.drawContours(img_biggest_contour, biggest, -1, (0, 255, 0), 5)
    return biggest_approx

def order_points(points):
    points = points.reshape((4,2))
    points_new = np.zeros((4,1,2),np.int32)
    add = points.sum(1)
    points_new[0] = points[np.argmin(add)]
    points_new[3] = points[np.argmax(add)]
    diff = np.diff(points,axis=1)
    points_new[1]= points[np.argmin(diff)]
    points_new[2] = points[np.argmax(diff)]
    return points_new

def get_warp(img, approx):
    approx = order_points(approx)
    pts1 = np.float32(approx)
    pts2 = np.float32([[0, 0], [FRAME_WIDTH, 0], [0, FRAME_HEIGHT], [FRAME_WIDTH, FRAME_HEIGHT]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    img_output = cv2.warpPerspective(img, matrix, (FRAME_WIDTH, FRAME_HEIGHT))
    
    img_cropped = img_output[20:img_output.shape[0]-20, 20:img_output.shape[1]-20]
    img_cropped = cv2.resize(img_cropped, (FRAME_WIDTH, FRAME_HEIGHT))
    return img_cropped

while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img = cv2.resize(img, (FRAME_WIDTH, FRAME_HEIGHT))
    
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (7, 7), 1)
    img_canny = cv2.Canny(img_blur, 75, 200)
    # cv2.imshow("Canny", img_canny)
    kernel = np.ones((5, 5))
    img_dialation = cv2.dilate(img_canny, kernel, iterations=2)
    img_eroded = cv2.erode(img_dialation, kernel, iterations=1)
    
    # img_eroded = get_img_treshold(img)
    img_contour = img.copy()
    img_biggest_contour = img.copy()
    
    biggest_contour = get_contours(img_eroded)
    img_warp = get_warp(img, biggest_contour) if biggest_contour.size else img.copy()
    
    img_stack = stack_images(0.5, ([img, img_gray, img_blur, img_canny],
                                   [img_eroded, img_contour, img_biggest_contour, img_warp]))
    cv2.imshow("Video", img_stack)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break