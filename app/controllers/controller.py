from flask import Response, render_template, redirect, url_for
from time import sleep
from app.models.rectangle import Rectangle
from app.models.webcam import Webcam
from app.models.analyze import Analyze


def configure(app):
    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route("/play_webcam")
    def play_webcam():
        return Response(webcam.generate(rectangle), mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/get_measures', methods = ['POST'])
    @app.route('/get_measures/<int:x1>/<int:y1>/<int:x2>/<int:y2>', methods = ['POST'])
    def get_measures(x1=None, y1=None, x2=None, y2=None):
        rectangle.get_measures(x1, y1, x2, y2)
        return ''

    @app.route('/clear_rectangle/', methods=['POST'])
    def clear_rectangle():
        rectangle.clear()
        return ''

    @app.route('/get_differentiator/', methods=['POST'])
    def get_differentiator():
        return analyze.get_differentiator(webcam, rectangle)

    @app.route('/start_analysis', methods=['POST'])
    def start_analysis():
        sleep(5)
        return redirect(url_for('teste'))

    @app.route('/teste/')
    def teste():
        return 'Deu certo'


webcam = Webcam()
rectangle = Rectangle()
analyze = Analyze()

