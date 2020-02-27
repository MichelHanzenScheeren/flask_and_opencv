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

