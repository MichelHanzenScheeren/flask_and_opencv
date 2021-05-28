# pylint: disable=unused-variable
from flask import Response, render_template, redirect, url_for, request


def configure_routes(app, appUseCase):
    """ Arquivo que cria e define as rotas relacionadas a página dos resultados da análise.

    O decorator @app.route define a rota http, e o método que segue define a resposta.
    """

    @app.route('/get_differentiator', methods=['POST'])
    def get_differentiator():
        return appUseCase.calculate_differentiator()

    @app.route('/get_differentiator_image', methods=['POST'])
    def get_differentiator_image():
        try:
            return Response(appUseCase.get_differentiator_image())
        except Exception as error:
            return appUseCase.error_response(error)

    @app.route('/start_analyze', methods=['POST'])
    def start_analyze():
        try:
            appUseCase.start_analyze(request.form)
            return redirect(url_for('results'))
        except:
            return redirect(url_for('error'))

    @app.route('/results')
    def results():
        try:
            return render_template('results.html', results=appUseCase.get_results(), page='results')
        except:
            return redirect(url_for('error'))

    @app.route('/get_all_images', methods=['POST'])
    def get_all_images():
        try:
            zip_file, headers = appUseCase.get_all_images()
            return Response(zip_file, headers=headers)
        except Exception as error:
            return appUseCase.error_response(error)

    @app.route('/get_xlsx_results', methods=['POST'])
    def get_xlsx_results():
        try:
            xlsx_file, headers = appUseCase.get_xlsx_results()
            return Response(xlsx_file, headers=headers)
        except Exception as error:
            return appUseCase.error_response(error)

    @app.route('/saveNewAnalyzeDate', methods=['POST'])
    @app.route('/saveNewAnalyzeDate/<string:newDate>', methods=['POST'])
    def saveNewAnalyzeDate(newDate=None):
        return appUseCase.saveNewAnalyzeDate(newDate)
