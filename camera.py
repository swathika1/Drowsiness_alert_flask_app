import cv2
from frame_processing_tools import process_frame, encode_to_jpeg


class VideoCamera:
    def __init__(self):  # constructor
        self.vid = cv2.VideoCapture(0)

    def __del__(self):  # destructor, no need for destroy windows as we are using webpage
        self.vid.release()

    def get_frame(self):
        success, frame = self.vid.read()
        frame = process_frame(frame)

        return encode_to_jpeg(frame)
