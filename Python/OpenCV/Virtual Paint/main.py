# PROJECT 1 : VIRTUAL PAINT

import cv2
import numpy as np

FRAME_WIDTH, FRAME_HEIGHT = 640//2, 480//2
cap = cv2.VideoCapture(0)
cap.set(3, FRAME_WIDTH)
cap.set(4, FRAME_HEIGHT)
cap.set(10, 150)

my_colors = [
    [135, 170, 110, 176, 255, 255], # pink
    [2, 211, 153, 10, 255, 255], # orange
    [68, 103, 0, 92, 255, 255], # green
    [25, 110, 0, 35, 240, 229] # yellow
]
my_color_values = [
    [71, 27, 178],
    [0, 45, 210],
    [76, 114, 34],
    [63, 163, 181]
]

my_points = [] # [x, y, colorID]

def find_color(img, colors, color_values):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    new_points = []
    for count, color in enumerate(colors):
        lower = np.array(color[:3])
        upper = np.array(color[3:])
        mask = cv2.inRange(img_hsv, lower, upper)
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        x, y = get_contours(mask)
        # cv2.circle(img_result, (x, y), 10, color_values[count], cv2.FILLED)
        # cv2.imshow(str(color[0]), mask)
        if x != 0 and y != 0:
            new_points.append([x, y, count])
    return new_points

def get_contours(img, area_treshold=500, points_treshold=0.02):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > area_treshold:
            # cv2.drawContours(img_result, cnt, -1, (255, 0, 0), 3)    
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, points_treshold*peri, True)
            obj_corners = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y

def draw_on_canvas(points, color_values):
    for point in points:
        cv2.circle(img_result, point[:2], 10, color_values[point[2]], cv2.FILLED)

while True:
    success, img = cap.read()
    
    img_result = img.copy()
    new_points = find_color(img, my_colors, my_color_values)
    my_points.extend(new_points)
    if my_points:
        draw_on_canvas(my_points, my_color_values)
    
    # cv2.imshow("Video", img)
    cv2.imshow("Result", cv2.resize(img_result, (640, 480)))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

