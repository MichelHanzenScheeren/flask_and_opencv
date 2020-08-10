# pylint: disable=unused-variable
from flask import Response, render_template, redirect, url_for, request
from time import sleep
from app.models.webcam import Webcam
from app.models.analyze import Analyze


def configure(app):
    @app.route('/')
    def index():
        webcam.init_webcam()
        return render_template("index.html", page="index")

    @app.route("/play_webcam")
    def play_webcam():
        return Response(webcam.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route("/upload_image", methods = ['POST'])
    def upload_image():
        webcam.save_uploaded_image(request.files["file"])
        return ''
        
    @app.route('/get_measures', methods = ['POST'])
    @app.route('/get_measures/<int:x1>/<int:y1>/<int:x2>/<int:y2>', methods = ['POST'])
    def get_measures(x1=None, y1=None, x2=None, y2=None):
        webcam.define_points_of_rectangle(x1, y1, x2, y2)
        return ''

    @app.route('/clear_rectangle/', methods=['POST'])
    def clear_rectangle():
        webcam.clear_rectangle_and_uploaded_image()
        return ''

    @app.route('/get_differentiator/', methods=['POST'])
    def get_differentiator():
        return analyze.get_differentiator(webcam)

    @app.route('/start_analysis', methods=['POST'])
    def start_analysis():
        total_time = request.form['time']
        captures_seg = request.form['qtd']
        if total_time.isdigit() and captures_seg.isdigit():
            analyze.start_analyze(int(total_time), int(captures_seg), webcam)
            return redirect(url_for('results'))
        else:
            return redirect(url_for('index'))

    @app.route('/results/')
    def results():
        if analyze.is_valid():
            webcam.clear()
            return render_template("results.html", results = analyze.results, page="results")
        return redirect(url_for('index'))
        


webcam = Webcam()
analyze = Analyze()

