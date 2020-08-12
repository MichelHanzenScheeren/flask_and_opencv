# pylint: disable=unused-variable
from flask import Response, render_template, redirect, url_for, request, send_file
from time import sleep
from app.models.webcam import Webcam
from app.models.analyze import Analyze


def configure(app):
    @app.route("/")
    @app.route("/home/")
    @app.route("/index/")
    def index():
        webcam.init_webcam()
        return render_template("index.html", page="index", frame_shape=webcam.get_frame_shape())


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
    

    @app.route('/get_differentiator_image/', methods=['POST'])
    def get_differentiator_image():
        return Response(analyze.get_differentiator_image(webcam))


    @app.route('/start_analysis', methods=['POST'])
    def start_analysis():
        analyze.start_analyze(request.form['time'], request.form['qtd'], request.form["description"], webcam)
        return redirect(url_for('results'))


    @app.route('/results/')
    def results():
        if analyze.is_valid():
            webcam.clear()
            return render_template("results.html", results = analyze.results, page="results")
        return redirect(url_for('index'))
        

webcam = Webcam()
analyze = Analyze()


