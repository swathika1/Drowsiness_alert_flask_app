import cv2
import imutils
from imutils import face_utils
import numpy as np
from scipy.spatial import distance as dist


def process_frame(frame, face_detector, facial_landmark_predictor):
    framewidth = 600

    frame = imutils.resize(frame, width=framewidth)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_rectangles = face_detector(gray_frame)  # it is easier to get face rectangle from greyscale image

    ear = -1.0

    for rect in face_rectangles:
        face_shape = facial_landmark_predictor(image=gray_frame, box=rect)
        left_eye, right_eye = eye_predictor(face_shape)
        draw_eyes(frame, left_eye, right_eye)
        ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0
        break  # assuming only one face needs detection as only one driver

    return frame, ear


def draw_eyes(frame, left_eye, right_eye):
    lefteye_hull = cv2.convexHull(left_eye)
    righteye_hull = cv2.convexHull(right_eye)
    cv2.drawContours(frame, [lefteye_hull], -1, (255, 0, 0), 1)
    cv2.drawContours(frame, [righteye_hull], -1, (255, 0, 0), 1)


def eye_predictor(face_shape):
    # predicting eye using face coordinates
    # making it into usable format to calculate EAR
    # left eye coordinates from 36 to 41

    left = str([face_shape.part(i) for i in get_point_numbers_of_feature('left_eye')])

    # right eye coordinates from 42 to 47
    right = str([face_shape.part(i) for i in get_point_numbers_of_feature('right_eye')])

    left = np.array(
        left.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('point', '').split(","),
        dtype=int).reshape(-1, 2)
    right = np.array(
        right.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('point', '').split(","),
        dtype=int).reshape(-1, 2)

    return left, right


def get_point_numbers_of_feature(feature: str) -> [int]:  # returns point numbers corresponding to a feature
    l, h = face_utils.FACIAL_LANDMARKS_IDXS[feature]
    return range(l, h)


def eye_aspect_ratio(eye):
    # vertical and horzontal distance within the eye

    vertical1 = dist.euclidean(eye[1], eye[5])
    vertical2 = dist.euclidean(eye[2], eye[4])

    horizontal = dist.euclidean(eye[0], eye[3])

    ear_value = (vertical1 + vertical2) / (2.0 * horizontal)

    return ear_value
