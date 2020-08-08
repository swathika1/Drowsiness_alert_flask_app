import cv2
import imutils

FRAMEWIDTH = 500


def process_frame(frame):
    frame = imutils.resize(frame, width=FRAMEWIDTH)
    # gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    return frame


def encode_to_jpeg(image):
    success, jpeg = cv2.imencode(".jpg", image)
    return jpeg.tobytes()  # returns byte array form of image which has been converted to jpeg
    # jpeg files are used in byte array form by web browsers
