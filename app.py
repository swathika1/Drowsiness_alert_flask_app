from flask import Flask, render_template, Response
from camera import VideoCamera

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")  # app route "/" delivers whatever is in its function


@app.route('/alert_system')
def alert_system():
    return render_template("alertsystem.html")


@app.route('/video_feed')
def video_feed():
    return Response(gen_jpeg_frame(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


"""mimetype is response media type, for the purpose of having a stream where each part replaces the previous
 part the multipart/x-mixed-replace content type must be used - here each frame is a part"""


# flask uses a generator function to implement streaming
def gen_jpeg_frame(vid_camera):  # generates jpeg frames from input stream
    while True:
        jpeg_byte_array = vid_camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg_byte_array + b'\r\n\r\n')


if __name__ == '__main__':
    app.run(debug=True)
