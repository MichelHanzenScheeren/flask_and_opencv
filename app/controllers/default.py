from flask import Response, render_template
from app.models.rectangle import Rectangle
from app.models.webcam import Webcam


def configure(app):
    @app.route('/')
    @app.route('/index/')
    def index():
        return render_template("index.html")

    @app.route("/play_webcam")
    def play_webcam():
        return Response(webcam.generate_jpg(rectangle), mimetype = "multipart/x-mixed-replace; boundary=frame")

    @app.route('/get_measures', methods = ['POST'])
    @app.route('/get_measures/<int:x1>/<int:y1>/<int:x2>/<int:y2>', methods = ['POST'])
    def get_measures(x1=None, y1=None, x2=None, y2=None):
        rectangle.get_measures(x1, y1, x2, y2)
        return 'OK'

    @app.route('/get_differentiator', methods=['POST'])
    def get_differentiator():
        while True:
            with webcam.lock_frame:
                frame = webcam.output_frame.copy()
            if frame is None:
                continue
            with rectangle.lock_drawing:
                media = (frame[rectangle.y_initial:rectangle.y_final, rectangle.x_initial:rectangle.x_final].mean(axis=0).mean(axis=0))
                return f' R = {media[2]}, G = {media[1]}, B = {media[0]}'


def stop_stream():
    webcam.stop_stream()


rectangle = Rectangle()
webcam = Webcam()
webcam.start()

