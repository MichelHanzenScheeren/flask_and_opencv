# pylint: disable=unused-variable
from flask import Response, render_template, redirect, url_for, request


def configure_routes(app, appUseCase):
    """ Arquivo que cria e define as rotas relacionadas a HomePage.

    O decorator @app.route define a rota http, e o método que segue define a resposta.
    """

    @app.route('/')
    @app.route('/index')
    @app.route('/home')
    def index():
        try:
            status, webcans_list = appUseCase.init_webcam()
            return render_template('index.html', page='index', video_status=status, webcans_list=webcans_list)
        except Exception:
            return redirect(url_for('error'))

    @app.route('/play_webcam')
    def play_webcam():
        return Response(appUseCase.webcam.stream_webcam(), mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/upload_image', methods=['POST'])
    def upload_image():
        return appUseCase.save_uploaded_image(request.files["file"])

    @app.route('/get_measures', methods=['POST'])
    @app.route('/get_measures/<int:x1>/<int:y1>/<int:x2>/<int:y2>', methods=['POST'])
    def get_measures(x1=None, y1=None, x2=None, y2=None):
        return appUseCase.define_points_of_rectangle(x1, y1, x2, y2)

    @app.route('/clear_rectangle', methods=['POST'])
    def clear_rectangle():
        return appUseCase.clear_rectangle_and_uploaded_image()

    @app.route('/change_current_webcam', methods=['POST'])
    @app.route('/change_current_webcam/<int:index_webcam>', methods=['POST'])
    def change_current_webcam(index_webcam=None):
        return appUseCase.change_current_webcam(index_webcam)
