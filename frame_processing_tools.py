import cv2
import dlib
import imutils
from imutils import face_utils
import numpy as np


FRAMEWIDTH = 400
FACIAL_SHAPE_PREDICTOR = "shape_predictor_68_face_landmarks.dat"


def process_frame(frame):
    frame = imutils.resize(frame, width=FRAMEWIDTH)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_detector = dlib.get_frontal_face_detector()  # returns face rectangle(s)
    facial_landmarks_predictor = dlib.shape_predictor(FACIAL_SHAPE_PREDICTOR)

    face_rectangles = face_detector(gray_frame)  # it is easier to get face rectangle from greyscale image

    for rect in face_rectangles:
        face_shape = facial_landmarks_predictor(image=gray_frame, box=rect)
        left_eye, right_eye = eye_predictor(face_shape)

        lefteye_hull = cv2.convexHull(left_eye)
        righteye_hull = cv2.convexHull(right_eye)
        cv2.drawContours(frame, [lefteye_hull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [righteye_hull], -1, (0, 255, 0), 1)

    return frame


def eye_predictor(face_shape):
    # predicting eye using face coordinates
    # making it into usable format to calculate EAR
    # left eye coordinates from 36 to 41

    left = str([face_shape.part(i) for i in get_point_numbers_of_feature('left_eye')])

    # right eye coordinates from42 to 47
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
