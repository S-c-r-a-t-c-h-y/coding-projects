import cv2
import numpy as np

def stack_images(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

def draw_contours(img, drawing_image, area_treshold=500, points_treshold=0.01):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > area_treshold:
            cv2.drawContours(drawing_image, cnt, -1, (255, 0, 0), 3)    
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, points_treshold*peri, True)
            # print(area, peri, sep=' - ')
            # print(len(approx))
            obj_corners = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
            
            object_type = "undefined"
            if obj_corners == 3:
                object_type = "triangle"
            elif obj_corners == 4:
                object_type = "square" if 0.95 <= w/float(h) <= 1.05 else "rectangle"
            elif obj_corners > 4:
                object_type = "circle"
            
            cv2.rectangle(drawing_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(drawing_image, object_type, 
                        (x + (w// 2) - 10, y + (h // 2) - 10), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)
    
    
def get_contours(img, area_treshold=500, points_treshold=0.01):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > area_treshold:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, points_treshold*peri, True)
            # obj_corners = len(approx)
            x, y, w, h = cv2.boundingRect(approx)

    
    