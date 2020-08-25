from flask import Flask, render_template, Response
from camera import VideoCamera
import cv2
from sound_tools import play_alarm_sound, break_suggest
import dlib


app = Flask(__name__)

EAR_THRESHOLD = 0.25
CONSECUTIVE_FRAMES_THRESHOLD = 20
BREAK_LIMIT = 4
SHAPE_PREDICTOR_FILE = "shape_predictor_68_face_landmarks.dat"


@app.route('/')
def home():
    return render_template("home.html")  # app route "/" delivers whatever is in its function


@app.route('/alert_system')
def alert_system():
    return render_template("alertsystem.html")


@app.route('/driving_tips')
def driving_tips():
    return render_template("driving_tips.html")


@app.route('/video_feed')
def video_feed():
    facial_shape_predictor = SHAPE_PREDICTOR_FILE
    face_detector = dlib.get_frontal_face_detector()
    facial_landmark_predictor = dlib.shape_predictor(facial_shape_predictor)

    return Response(gen_jpeg_frame(VideoCamera(face_detector, facial_landmark_predictor)), mimetype='multipart/x'
                                                                                                    '-mixed-replace; '
                                                                                                    'boundary=frame')


"""mimetype is response media type, for the purpose of having a stream where each part replaces the previous
 part the multipart/x-mixed-replace content type must be used - here each frame is a part"""


# flask uses a generator function to implement streaming
def gen_jpeg_frame(vid_camera):  # generates jpeg frames from input stream
    # counting number of frames to play alert sound
    frame_count = 0
    break_count = 0

    while True:
        frame, ear = vid_camera.get_frame()
        if frame is None:
            continue

        success, jpeg = cv2.imencode(".jpg", frame)

        if not success:
            continue

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

        if ear < 0:
            continue

        if ear <= EAR_THRESHOLD:
            frame_count += 1

            if frame_count >= CONSECUTIVE_FRAMES_THRESHOLD:
                break_count += 1
                play_alarm_sound()
                frame_count = 0
                if break_count >= BREAK_LIMIT:
                    break_suggest()
                    break_count = 0

        else:
            frame_count = 0


if __name__ == '__main__':
    app.run(debug=True)
