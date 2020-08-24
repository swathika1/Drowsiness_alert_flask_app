import cv2
from frame_processing_tools import process_frame


class VideoCamera:

    def __init__(self, fd, flp):  # constructor
        self.vid = cv2.VideoCapture(0)
        self.fd = fd
        self.flp = flp

    def __del__(self):  # destructor, no need for destroy windows as we are using webpage
        self.vid.release()

    def get_frame(self):
        success, frame = self.vid.read()
        frame = process_frame(frame, self.fd, self.flp)

        return frame
