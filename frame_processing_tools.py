import cv2
import imutils
import dlib

FRAMEWIDTH = 500


def process_frame(frame):
    frame = imutils.resize(frame, width=FRAMEWIDTH)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_detector = dlib.get_frontal_face_detector()  # returns face rectangle(s)
    face_rectangles = face_detector(gray_frame)  # it is easier to get face rectangle from greyscale image
    for rect in face_rectangles:
        cv2.rectangle(img=frame, pt1=(rect.left(), rect.top()), pt2=(rect.right(), rect.bottom()), color=(0, 0, 255), thickness=2)
    return frame


def encode_to_jpeg(image):
    success, jpeg = cv2.imencode(".jpg", image)
    return jpeg.tobytes()  # returns byte array form of image which has been converted to jpeg
    # jpeg files are used in byte array form by web browsers
