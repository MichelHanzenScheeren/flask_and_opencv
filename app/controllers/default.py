from flask import Response, render_template
from app.models.rectangle import Rectangle
from app.models.webcam import Webcam
from app.models.analyze import Analyze


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
        return analyze.get_differentiator(webcam, rectangle)



def stop_stream():
    webcam.stop_stream()



webcam = Webcam()
webcam.start()
rectangle = Rectangle()
analyze = Analyze()

