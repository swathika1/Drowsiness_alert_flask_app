# import the necessary packages
# SciPy to use for eucledian distance btw eyes
from scipy.spatial import distance as dist
import numpy as np
# alert sound
import sounddevice as sdevice
import soundfile as sfile

# time.sleep() suspends excecution of prog for specified amt of time
import time

# dlib to detect facial landmarks
import dlib
import cv2

# alarm to alert
SoundTrack = "loud_alarm.wav"


def eye_aspect_ratio(eye):
    # vertical and horzontal distance within the eye

    vertical1 = dist.euclidean(eye[1], eye[5])
    vertical2 = dist.euclidean(eye[2], eye[4])

    horizontal = dist.euclidean(eye[0], eye[3])

    EAR_value = (vertical1 + vertical2) / (2.0 * horizontal)

    return EAR_value


def play_alarm_sound():
    # reading alarm file
    data, sound = sfile.read(SoundTrack)
    sdevice.play(data, sound)


# Maximum limit for EAR value for a normal eye

Threshold_value = 0.3

# maximum frame limit for the alarm to ring for a drowsy user

warning_limit = 35

# detecting face
detected_face = dlib.get_frontal_face_detector()
predict_points = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


def eye_predictor(face_shape):
    # predicting eye using face coordinates
    # making it into usable format to calculate EAR
    # left eye coordinates from 36 to 41

    left = str([face_shape.part(36), face_shape.part(37), face_shape.part(38), face_shape.part(39), face_shape.part(40),
                face_shape.part(41)])

    # right eye coordinates from42 to 47
    right = str(
        [face_shape.part(42), face_shape.part(43), face_shape.part(44), face_shape.part(45), face_shape.part(46),
         face_shape.part(47)])
    left = np.array(
        left.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('point', '').split(","),
        dtype=int).reshape(-1, 2)
    right = np.array(
        right.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('point', '').split(","),
        dtype=int).reshape(-1, 2)

    return left, right


# counting number of frames to play alert sound
frame_count = 0


def drowsiness_detect():
    # 0 key keeps the camera open for as long as user requires
    vid = cv2.VideoCapture(0)
    frame_count = 0
    while (True):
        sucess, img = vid.read()

        gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces_detected = detected_face(gray_scale, 0)

        for face in faces_detected:
            face_shape = predict_points(gray_scale, face)
            left_eye, right_eye = eye_predictor(face_shape)
            # drawing contours and obtaining eye

            lefteye_hull = cv2.convexHull(left_eye)
            righteye_hull = cv2.convexHull(right_eye)
            cv2.drawContours(img, [lefteye_hull], -1, (0, 0, 255), 1)
            cv2.drawContours(img, [righteye_hull], -1, (0, 0, 255), 1)

            # obtaining ear aspect ratio average from both eyes
            EAR = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0
            if EAR <= Threshold_value:
                frame_count += 1
                if (frame_count >= warning_limit):
                    # display alert message on frame
                    cv2.putText(img, "DROWSINESS DETECTED ALERT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0),
                                2)
                    play_alarm_sound()
                    frame_count = 0
            else:
                frame_count = 0
            # Display the EAR on the frame with precision upto two decimal places
            cv2.putText(img, "EAR : {:.2f}".format(EAR), (400, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow('DROWSINESS DETECTION MODE', img)


        if (cv2.waitKey(1) & 0xFF == ord("q")):  # closes camera when 'q' is pressed
            cv2.destroyAllWindows()
            vid.release()
            break


drowsiness_detect()
