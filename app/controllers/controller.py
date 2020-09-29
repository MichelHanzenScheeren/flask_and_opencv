# pylint: disable=unused-variable
from flask import Response, render_template, redirect, url_for, request
from time import sleep
from app.models.webcam import Webcam
from app.models.analyze import Analyze


def configure(app):
    @app.route("/")
    def index():
        try:
            webcam.init_webcam()
            return render_template("index.html", page="index", 
                video_status=webcam.video_status(), webcans_list=webcam.webcans_list())
        except Exception as exception:
            print(exception)
            return redirect(url_for('error'))


    @app.route("/play_webcam")
    def play_webcam():
        return Response(webcam.generate_images(), mimetype='multipart/x-mixed-replace; boundary=frame')


    @app.route("/upload_image", methods = ['POST'])
    def upload_image():
        webcam.save_uploaded_image(request.files["file"])
        return ''


    @app.route('/get_measures', methods = ['POST'])
    @app.route('/get_measures/<int:x1>/<int:y1>/<int:x2>/<int:y2>', methods = ['POST'])
    def get_measures(x1=None, y1=None, x2=None, y2=None):
        webcam.rectangle.define_points_of_rectangle(x1, y1, x2, y2)
        return ''


    @app.route('/clear_rectangle', methods=['POST'])
    def clear_rectangle():
        webcam.clear_rectangle_and_uploaded_image()
        return ''
    

    @app.route('/change_current_webcam', methods = ['POST'])
    @app.route('/change_current_webcam/<int:index_webcam>', methods = ['POST'])
    def change_current_webcam(index_webcam=None):
        return webcam.change_current_webcam(index_webcam)


    @app.route('/get_differentiator', methods=['POST'])
    def get_differentiator():
        analyze.clear()
        return analyze.get_differentiator(webcam)


    @app.route('/start_analysis', methods=['POST'])
    def start_analysis():
        try:
            time, qtd, desc = request.form['time'],request.form['qtd'],request.form["description"]
            analyze.start_analyze(time, qtd, desc, webcam)
            return redirect(url_for('results'))
        except:
            return redirect(url_for('error'))


    @app.route('/results')
    def results():
        try:
            return render_template("results.html", results = analyze.results, page="results")
        except:
            return redirect(url_for('error'))
            

    @app.route('/get_differentiator_image', methods=['POST'])
    def get_differentiator_image():
        return Response(analyze.results.get_differentiator_image())
    

    @app.route('/get_all_images', methods=['POST'])
    def get_all_images():
        zip_file = analyze.results.get_all_images()
        headers = {'content-type': 'application/zip', 'format': 'base64', 'file-name': 'imagens.zip'}
        return Response(zip_file, headers = headers)
    

    @app.route('/get_xlsx_results', methods=['POST'])
    def get_xlsx_results():
        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        headers = {'content-type': content_type, 'format': 'base64', 'file-name': 'resultados.xlsx'}
        return Response(analyze.results.get_xlsx_results(), headers = headers)
    

    @app.route("/error")
    def error():
        return render_template("error.html", page="error")


webcam = Webcam()
analyze = Analyze()


