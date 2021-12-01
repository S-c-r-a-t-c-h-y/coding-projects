import cv2
from hand_tracking_module import hand_detector
import numpy as np
import hand_tracking_module as htm
import ctypes
import math
import time

user32 = ctypes.windll.user32
SYSTEM_WIDTH, SYSTEM_HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def get_tendancy_curve(x_values, y_values):
    """Returns the tendancy curve of a set of points of coords
    x_values[n], y_values[n]"""

    n = len(x_values)
    try:
        a = (sum(x * y for x, y in zip(x_values, y_values)) - (sum(x_values) * sum(y_values) / n)) / (
            sum(x ** 2 for x in x_values) - (sum(x_values) ** 2) / n
        )
        b = sum(y_values) / n - a * (sum(x_values) / n)
    except ZeroDivisionError:
        a, b = 0, 0

    return a, b


SMOOTHENING = 7
plocX, plocY = 0, 0
clocX, clocY = 0, 0

p_time = 0
c_time = 0

WIDTH, HEIGHT = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, WIDTH)
cap.set(4, HEIGHT)

detector = htm.hand_detector(max_hands=1, detection_con=0.3, track_con=0.9, model_complexity=1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.find_hands(img, draw=True)
    lm_list = detector.find_position(img, draw=True)

    # c_time = time.time()
    # fps = 1 / (c_time - p_time)
    # p_time = c_time

    if len(lm_list) != 0:
        finger_points = [(x, y) for _, x, y in lm_list[5:9]]

        x_values = [x for x, _ in finger_points]
        y_values = [y for _, y in finger_points]

        a, b = get_tendancy_curve(x_values, y_values)

        angle = math.degrees(math.atan(-a))
        if x_values[0] > x_values[3]:
            angle += 180
        elif angle < 0:
            angle = 360 - abs(angle)

        # straight, _ = detector.finger_is_straight(img, 1, draw=False)
        max_length = 120

        percent_extension = np.interp(
            (math.hypot(x_values[3] - x_values[0], y_values[3] - y_values[0])), [50, max_length], [0, 1]
        )

        root_x, root_y = finger_points[0]
        if percent_extension == 0:
            intersec_x, intersec_y = root_x, root_y
        else:
            intersec1 = (WIDTH, a * WIDTH + b) if 0 <= angle <= 90 or 270 <= angle <= 360 else (0, b)
            intersec2 = ((-b) / a, 0) if 0 <= angle <= 180 else ((HEIGHT - b) / a, HEIGHT)

            dst1, dst2 = math.hypot(root_x - intersec1[0], root_y, intersec1[1]), math.hypot(
                root_x - intersec2[0], root_y, intersec2[1]
            )
            intersection = intersec1 if dst1 < dst2 else intersec2

            intersec_x, intersec_y = intersection

        x1, y1 = 0, int(b)
        x2, y2 = int(WIDTH), int(a * WIDTH + b)

        new_x, new_y = (
            int(root_x + (intersec_x - root_x) * percent_extension),
            int(root_y + (intersec_y - root_y) * percent_extension),
        )

        cv2.circle(img, (new_x, new_y), 10, (0, 255, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

        new_x = int(
            np.interp(
                new_x,
                [0, WIDTH],
                [0, SYSTEM_WIDTH],
            )
        )
        new_y = int(
            np.interp(
                new_y,
                [0, HEIGHT],
                [0, SYSTEM_HEIGHT],
            )
        )

        clocX = plocX + (new_x - plocX) / SMOOTHENING
        clocY = plocY + (new_y - plocY) / SMOOTHENING

        user32.SetCursorPos(int(clocX), int(clocY))
        plocX, plocY = clocX, clocY

    # cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Virtual Pointer", img)
    if cv2.waitKey(1) & 0xFF == ord("s"):
        break
