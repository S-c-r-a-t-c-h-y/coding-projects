import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


def stack_images(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale
                    )
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def get_bbox(x_values, y_values, margin=0):
    return min(x_values) - margin, min(y_values) - margin, max(x_values) + margin, max(y_values) + margin


left_eye_indices = [33, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7]
right_eye_indices = [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382]

left_eye_vertical_center_indices = [159, 145]
right_eye_vertical_center_indices = [386, 374]

left_eye_horizontal_center_indices = [33, 173]
right_eye_horizontal_center_indices = [398, 263]

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)
cap.set(10, 200)

params = cv2.SimpleBlobDetector_Params()

params.minThreshold = 20

params.filterByArea = True
params.maxArea = 1000

detector = cv2.SimpleBlobDetector_create(params)


def blob_process(img, detector):
    img = cv2.erode(img, (5, 5), iterations=2)  # 1
    img = cv2.dilate(img, (5, 5), iterations=4)  # 2
    img = cv2.medianBlur(img, 5)  # 3
    keypoints = detector.detect(img)
    return keypoints


def empty(a):
    pass


cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", (640, 70))

cv2.createTrackbar("Threshold 1", "TrackBars", 69, 255, empty)
cv2.createTrackbar("Threshold 2", "TrackBars", 127, 255, empty)

with mp_face_mesh.FaceMesh(
    max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5
) as face_mesh:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue
        image = cv2.flip(image, 1)

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)

        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if faces := results.multi_face_landmarks:

            shape = image.shape
            left_eye_coords = [
                (int((landmark := faces[0].landmark[i]).x * shape[1]), int(landmark.y * shape[0]), landmark.z)
                for i in left_eye_indices
            ]
            right_eye_coords = [
                (int((landmark := faces[0].landmark[i]).x * shape[1]), int(landmark.y * shape[0]), landmark.z)
                for i in right_eye_indices
            ]

            bbox_offset = 3
            x1, y1, x2, y2 = get_bbox(
                [x for x, _, _ in left_eye_coords], [y for _, y, _ in left_eye_coords], bbox_offset
            )
            x3, y3, x4, y4 = get_bbox(
                [x for x, _, _ in right_eye_coords], [y for _, y, _ in right_eye_coords], bbox_offset
            )

            z_min, z_max = min(z for _, _, z in left_eye_coords), max(z for _, _, z in left_eye_coords)
            # print(z_min, z_max)

            threshold1 = cv2.getTrackbarPos("Threshold 1", "TrackBars")
            threshold2 = cv2.getTrackbarPos("Threshold 2", "TrackBars")

            eye1, eye2 = image[y1:y2, x1:x2], image[y3:y4, x3:x4]
            eye1, eye2 = cv2.cvtColor(eye1, cv2.COLOR_BGR2GRAY), cv2.cvtColor(eye2, cv2.COLOR_BGR2GRAY)
            eye1, eye2 = cv2.GaussianBlur(eye1, (3, 3), 0.5), cv2.GaussianBlur(eye2, (3, 3), 0.5)
            eye1, eye2 = cv2.Canny(eye1, threshold1, threshold2), cv2.Canny(eye2, threshold1, threshold2)

            contours, hierarchy = cv2.findContours(eye1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            eye1 = cv2.cvtColor(eye1, cv2.COLOR_GRAY2BGR)
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 10:
                    cv2.drawContours(eye1, cnt, -1, (255, 0, 0), 1)
                    peri = cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

            # eye1 = cv2.erode(eye1, (5, 5), iterations=1)  # 1
            # eye1 = cv2.dilate(eye1, (5, 5), iterations=1)  # 2

            # _, eye1 = cv2.threshold(eye1, threshold1, 255, cv2.THRESH_BINARY)
            # _, eye2 = cv2.threshold(eye2, threshold2, 255, cv2.THRESH_BINARY)

            # keypoints1 = blob_process(eye1, detector)
            # keypoints2 = blob_process(eye2, detector)

            # eye1 = cv2.drawKeypoints(
            #     eye1, keypoints1, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
            # )
            # eye2 = cv2.drawKeypoints(
            #     eye2, keypoints2, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
            # )

            ratio = (y2 - y1) / (x2 - x1)
            eye1, eye2 = cv2.resize(eye1, (300, int(300 * ratio))), cv2.resize(eye2, (300, int(300 * ratio)))

            cv2.imshow("Eye 1", eye1)
            cv2.imshow("Eye 2", eye2)

            ### DRAWING ON THE MAIN IMAGE ###
            #################################

            for x, y, z in left_eye_coords:
                cv2.circle(
                    image, (x, y), radius=1, color=(0, int(np.interp(z, [z_min, z_max], [0, 255])), 0), thickness=1
                )

            for x, y, z in right_eye_coords:
                cv2.circle(
                    image, (x, y), radius=1, color=(0, int(np.interp(z, [z_min, z_max], [0, 255])), 0), thickness=1
                )

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(image, (x3, y3), (x4, y4), (0, 0, 255), 2)

            (x5, y5), (x6, y6) = [
                (int((landmark := faces[0].landmark[i]).x * shape[1]), int(landmark.y * shape[0]))
                for i in left_eye_vertical_center_indices
            ]

            (x7, y7), (x8, y8) = [
                (int((landmark := faces[0].landmark[i]).x * shape[1]), int(landmark.y * shape[0]))
                for i in left_eye_horizontal_center_indices
            ]

            cv2.line(image, (x5, y5), (x6, y6), (255, 0, 0), 1)
            cv2.line(image, (x7, y7), (x8, y8), (255, 0, 0), 1)

            (x9, y9), (x10, y10) = [
                (int((landmark := faces[0].landmark[i]).x * shape[1]), int(landmark.y * shape[0]))
                for i in right_eye_vertical_center_indices
            ]

            (x11, y11), (x12, y12) = [
                (int((landmark := faces[0].landmark[i]).x * shape[1]), int(landmark.y * shape[0]))
                for i in right_eye_horizontal_center_indices
            ]

            cv2.line(image, (x9, y9), (x10, y10), (255, 0, 0), 1)
            cv2.line(image, (x11, y11), (x12, y12), (255, 0, 0), 1)

            # for face_landmarks in faces:
            #     mp_drawing.draw_landmarks(
            #         image=image,
            #         landmark_list=face_landmarks,
            #         connections=mp_face_mesh.FACEMESH_TESSELATION,
            #         landmark_drawing_spec=None,
            #         connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style(),
            #     )
            #     # mp_drawing.draw_landmarks(
            #     #     image=image,
            #     #     landmark_list=face_landmarks,
            #     #     connections=mp_face_mesh.FACEMESH_CONTOURS,
            #     #     landmark_drawing_spec=None,
            #     #     connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style(),
            #     # )
            #     # mp_drawing.draw_landmarks(
            #     #     image=image,
            #     #     landmark_list=face_landmarks,
            #     #     connections=mp_face_mesh.FACEMESH_IRISES,
            #     #     landmark_drawing_spec=None,
            #     #     connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style(),
            #     # )

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow("MediaPipe Face Mesh", image)
        if cv2.waitKey(5) & 0xFF == ord("s"):
            break
cap.release()
print("stopped")
