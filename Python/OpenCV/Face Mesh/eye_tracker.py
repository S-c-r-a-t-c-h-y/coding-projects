# TODO: Get the right eye as well, and quantify position of pupil relative to the other eye keypoints


import numpy as np
import cv2
from imutils import face_utils
from imutils.video import VideoStream
import dlib
import time
import numpy as np

# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
vs = VideoStream(src=0).start()
time.sleep(2.0)
numerator = 0
denominator = 0

# create dlib faces detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
# eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = np.linalg.norm(eye[0] - eye[3])

    # calculates and return the eye aspect ratio
    return (A + B) / (2.0 * C)


def calculate_function(keypoints):
    for i in range(0, 8, 2):
        lx, ly = keypoints[i]
        rx, ry = keypoints[i + 1]
        print(lx, ly, rx, ry)


keypoints: list[tuple[float, float]] = []

while True:
    key = cv2.waitKey(1) & 0xFF

    frame = vs.read()
    frame = cv2.flip(frame, 1)  # flips the frame

    roi = frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect dlib face rectangles in the grayscale frame
    dlib_faces = detector(gray, 0)

    # loop through each face
    for face in dlib_faces:

        # store 2 eyes here
        eyes = []

        # convert dlib rect to a bounding box
        (x, y, w, h) = face_utils.rect_to_bb(face)
        # print(x,y,w,h)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)

        # get the landmarks from dlib, convert to np array
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[lStart:lEnd]  # indexes for left eye key points
        rightEye = shape[rStart:rEnd]  # indexes for right eye key points

        eyes.append(leftEye)  # wrap in a list
        eyes.append(rightEye)

        # save the state of both eyes to print
        both_eyes_state = []

        # loop through both eyes
        for index, eye in enumerate(eyes):

            eye_EAR = eye_aspect_ratio(eye)

            single_eye_state = (
                []
            )  # first entry is eye index, second entry is the closed or eye direction state

            left_side_eye = eye[0]  # left edge of eye
            right_side_eye = eye[3]  # right edge of eye
            top_side_eye = eye[1]  # top side of eye
            bottom_side_eye = eye[4]  # bottom side of eye

            # calculate height and width of dlib eye keypoints
            eye_width = right_side_eye[0] - left_side_eye[0]
            eye_height = bottom_side_eye[1] - top_side_eye[1]

            # create bounding box with buffer around keypoints
            eye_x1 = int(left_side_eye[0] - 0 * eye_width)  # .25 works well too
            eye_x2 = int(right_side_eye[0] + 0 * eye_height)  # .75 works well too

            eye_y1 = int(top_side_eye[1] - 1 * eye_height)
            eye_y2 = int(bottom_side_eye[1] + 1 * eye_height)

            # draw bounding box around eye roi
            cv2.rectangle(frame, (eye_x1, eye_y1), (eye_x2, eye_y2), (0, 255, 0), 2)

            # draw the circles for the eye landmarks
            for i in eye:
                cv2.circle(frame, tuple(i), 3, (0, 0, 255), -1)

            # ------------ estimation of distance of the human from camera--------------#
            # d=10920.0/float(w)

            roi = frame[eye_y1:eye_y2, eye_x1:eye_x2]

            #  ---------    check if eyes open   -------------  #

            # state is open/close, or direction looking
            eye_state = None

            # the eye is opened
            if eye_EAR > 0.25:

                #  ---------    find center of pupil   -------------  #

                gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)  # grey scale convert
                blur = cv2.medianBlur(gray, 5)  # blue image to find the iris better
                equ = cv2.equalizeHist(
                    blur
                )  # ie, improve contrast by spreading the range over the same window of intensity
                thres = cv2.inRange(
                    equ, 0, 15
                )  # threshold the contour edges, higher number means more will be black
                kernel = np.ones((3, 3), np.uint8)  # placeholder

                #     #/------- removing small noise inside the white image ---------/#
                dilation = cv2.dilate(thres, kernel, iterations=2)
                #     #/------- decreasing the size of the white region -------------/#
                erosion = cv2.erode(dilation, kernel, iterations=3)
                #     #/-------- finding the contours -------------------------------/#
                # image, contours, hierarchy = cv2.findContours(erosion,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
                contours, hierarchy = cv2.findContours(
                    erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
                )
                #     #--------- checking for 2 contours found or not ----------------#

                pupil_found = None

                if len(contours) == 2:
                    # print('2 contours found')
                    pupil_found = True

                    img = cv2.drawContours(roi, contours, 1, (0, 255, 0), 3)
                    # ------ finding the centroid of the contour ----------------#
                    M = cv2.moments(contours[1])

                    if M["m00"] != 0:
                        cx = M["m10"] / M["m00"]
                        cy = M["m01"] / M["m00"]
                        cv2.line(
                            roi, (int(cx), int(cy)), (int(cx), int(cy)), (0, 0, 255), 3
                        )
                # -------- checking for one contour present --------------------#

                if len(contours) == 1:
                    pupil_found = True
                    # print('only 1 contour found ------- ')

                    img = cv2.drawContours(roi, contours, 0, (0, 255, 0), 3)

                    # ------- finding centroid of the contour ----#
                    M = cv2.moments(contours[0])
                    if M["m00"] != 0:
                        cx = M["m10"] / M["m00"]
                        cy = M["m01"] / M["m00"]
                        cv2.line(
                            roi, (int(cx), int(cy)), (int(cx), int(cy)), (0, 0, 255), 3
                        )

                if pupil_found:

                    if key == ord("p"):
                        if len(keypoints) < 4 * 2:
                            keypoints.append((cx, cy))
                            print(keypoints)
                        else:
                            calculate_function(keypoints)

                    # find ratio of distance from each side of the eye bounding box
                    # to get quantify direction of pupil

                    width_ratio = cx / eye_width
                    height_ratio = cy / (
                        eye_y2 - eye_y1
                    )  # make sure to use bounding box height

                    if width_ratio < 0.4:
                        single_eye_state.append(index)
                        single_eye_state.append("Right")
                    elif width_ratio > 0.6:
                        single_eye_state.append(index)
                        single_eye_state.append("Left")
                    elif height_ratio < 0.35:
                        single_eye_state.append(index)
                        single_eye_state.append("Up")
                    else:
                        single_eye_state.append(index)
                        single_eye_state.append("Forward")

                # eyes are opened, but pupils not found
                else:
                    single_eye_state.append(index)
                    single_eye_state.append("No pupil found")

            # if height / width < 0.25, then eye is closed, or person is looking down
            else:
                single_eye_state.append(index)
                single_eye_state.append("Closed")

            # end loop for one eye
            both_eyes_state.append(single_eye_state)

        # end loop for one face
        # write state for both eyes

        # for ind, eye in enumerate(both_eyes_state):
        #     # print(eye)
        #     eye_num = ["Left", "Right"]
        #     # text = 'Hello'
        #     text = "{} eye is looking:  {}".format(eye_num[ind], eye[1])
        #     cv2.putText(
        #         frame,
        #         text,
        #         (0, 50 * (ind + 1)),
        #         cv2.FONT_HERSHEY_SIMPLEX,
        #         1.5,
        #         (0, 0, 255),
        #         2,
        #     )

    cv2.imshow("frame", frame)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
vs.release()
# print("accurracy=",(float(numerator)/float(numerator+denominator))*100)
cv2.destroyAllWindows()
