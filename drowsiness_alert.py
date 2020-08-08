import cv2
import dlib
import imutils
from imutils import face_utils
import sounddevice as sdevice
import soundfile as sfile
from scipy.spatial import distance


FACIAL_SHAPE_PREDICTOR = "shape_predictor_68_face_landmarks.dat"
ALARM = "loud_alarm.wav"
EAR_THRESHOLD = 0.3
CONSECUTIVE_FRAMES_THRESHOLD = 30
FRAMEWIDTH=500


def run_detector():
    vidcapture = cv2.VideoCapture(0)  # video capture object, video captured from webcam-0

    key = ""

    face_detector = dlib.get_frontal_face_detector()  # returns face rectangle(s)
    facial_landmarks_predictor = dlib.shape_predictor(FACIAL_SHAPE_PREDICTOR)
    # given an image and the face rectangle, the facial_landmark_predictor returns
    # the coordinates of the facial landmarks as per the given template
    no_of_frames_eyes_drooped = 0

    while key != 27:  # 27 corresponds to the escape key
        success, frame = vidcapture.read()
        if not success:
            print("Camera Disconnected!")
            break

        frame = imutils.resize(frame, width=FRAMEWIDTH)
        grey_frame = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)
        face_rectangles = face_detector(grey_frame)  # it is easier to get face rectangle from greyscale image

        for face_rectangle in face_rectangles:
            face_landmarks = facial_landmarks_predictor(image=grey_frame, box=face_rectangle)
            display_feature_landmarks(frame, 'left_eye', face_landmarks)
            display_feature_landmarks(frame, 'right_eye', face_landmarks)  # to show the eye landmark points

            ear_left = eye_aspect_ratio(face_landmarks, get_point_numbers_of_feature('left_eye'))
            ear_right = eye_aspect_ratio(face_landmarks, get_point_numbers_of_feature('right_eye'))
            ear_avg = (ear_left + ear_right) / 2.0

            cv2.putText(img=frame, text="EAR: " + str(ear_avg), org=(FRAMEWIDTH - 200, 20), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255))

            # as droopiness increases and horizontal nature of eye decreases, EAR decreases
            if ear_avg < EAR_THRESHOLD:
                no_of_frames_eyes_drooped += 1
                if no_of_frames_eyes_drooped >= CONSECUTIVE_FRAMES_THRESHOLD:
                    play_alarm_sound(ALARM)
                    no_of_frames_eyes_drooped = 0
            else:
                no_of_frames_eyes_drooped = 0  # eyes closed for short time but now open, so reset counter to zero

        cv2.imshow(winname="Drowsiness Alert System", mat=frame)  # display frame

        key = cv2.waitKey(1)

    # release video capture and close open windows
    vidcapture.release()  # Closes video file or capturing device
    cv2.destroyAllWindows()  # destroys the specified windows


def display_feature_landmarks(frame, feature: str, face_landmarks):
    for i in get_point_numbers_of_feature(feature):
        x, y = face_landmarks.part(i).x, face_landmarks.part(i).y
        cv2.circle(img=frame, center=(x, y), color=(255, 0, 0), radius=1, thickness=-1)
        # this adds a circle on the frame with center at teh facial landmark and
        # thickness = -1 which means it is a solid circle


def get_point_numbers_of_feature(feature: str) -> [int]:  # returns point numbers corresponding to a feature
    l, h = face_utils.FACIAL_LANDMARKS_IDXS[feature]
    return range(l, h)


def play_alarm_sound(soundtrack):
    # reading alarm file
    data, sound = sfile.read(soundtrack)
    sdevice.play(data, sound)


def eye_aspect_ratio(landmarks, eye_landmark_numbers):
    left_corner_coords = landmarks.part(eye_landmark_numbers[0]).x, landmarks.part(eye_landmark_numbers[0]).y
    right_corner_coords = landmarks.part(eye_landmark_numbers[3]).x, landmarks.part(eye_landmark_numbers[3]).y

    top_left_coords = landmarks.part(eye_landmark_numbers[1]).x, landmarks.part(eye_landmark_numbers[1]).y
    top_right_coords = landmarks.part(eye_landmark_numbers[2]).x, landmarks.part(eye_landmark_numbers[2]).y

    bottom_left_coords = landmarks.part(eye_landmark_numbers[5]).x, landmarks.part(eye_landmark_numbers[5]).y
    bottom_right_coords = landmarks.part(eye_landmark_numbers[4]).x, landmarks.part(eye_landmark_numbers[4]).y

    vertical_dist1 = distance.euclidean(top_left_coords, bottom_left_coords)
    vertical_dist2 = distance.euclidean(top_right_coords, bottom_right_coords)
    horizontal_dist = distance.euclidean(left_corner_coords, right_corner_coords)
    return (vertical_dist1 + vertical_dist2) / (2.0 * horizontal_dist)


run_detector()
