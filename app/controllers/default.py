from flask import Response, render_template
from app.models.rectangle import Rectangle
from app.models.webcam import Webcam
"""
from imutils.video import VideoStream
from imutils import resize
from threading import Thread, Lock
import cv2.cv2 as cv2
"""

def configure(app):
    @app.route('/')
    @app.route('/index/')
    def index():
        return render_template("index.html")


    @app.route("/play_webcam")
    def play_webcam():
        return Response(webcam.generate_jpg(rectangle), mimetype = "multipart/x-mixed-replace; boundary=frame")


    @app.route('/drawing', methods = ['POST'])
    @app.route('/drawing/<int:x1>/<int:y1>/<int:x2>/<int:y2>', methods = ['POST'])
    def get_measures(x1=None, y1=None, x2=None, y2=None):
        rectangle.get_measures(x1, y1, x2, y2)
        return 'OK'


def stop_stream():
    webcam.stop_stream()


rectangle = Rectangle()
webcam = Webcam()
webcam.start()
"""
def get_image():
    global vs, outputFrame, lock_frame
    while True:
        frame = vs.read()  # obtêm frame da Webcam
        #frame = vs.read()[1]
        frame = cv2.flip(frame, 1)  # espelha a imagem
        frame = resize(frame, width=520)  # redimensiona
        #frame = retangulo(frame)
        with lock_frame:
            outputFrame = frame.copy()


def generate():
    global outputFrame, lock_frame
    while True:
        with lock_frame:
            if outputFrame is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", draw_rectangle(outputFrame.copy())) # encode the frame in JPEG format
            if not flag: # ensure the frame was successfully encoded
                continue
        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')


def draw_rectangle(frame):
    global x_inicio, x_fim, y_inicio, y_fim
    with lock_drawing:
        if x_inicio != -1 and x_fim != -1:
            cv2.rectangle(frame, (x_inicio, y_inicio), (x_fim, y_fim), (0, 0, 255), 1)
    return frame


def stop_stream():
    global vs
    vs.stop()

x_inicio, y_inicio, x_fim, y_fim = -1, -1, -1, -1

outputFrame = None
lock_frame = Lock()
lock_drawing = Lock()

vs = VideoStream(src=0).start() #vs = cv2.VideoCapture(0)

t = Thread(target=get_image, daemon=True)
t.start()
"""
