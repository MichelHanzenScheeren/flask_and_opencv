from app.configuration import NUMBER_OF_VALVES
from flask import Response, render_template, redirect, url_for, request
import json


def configure_routes(app, analyzeUseCase):
    """ Arquivo que cria e define as rotas relacionadas a página dos resultados da análise.

    O decorator @app.route define a rota http, e o método que segue define a resposta.
    """

    @app.route('/get_differentiator', methods=['POST'])
    def get_differentiator():
        return analyzeUseCase.calculate_differentiator()

    @app.route('/start_analyze', methods=['POST'])
    def start_analyze():
        analyzeUseCase.start_analyze(request.form)
        return redirect(url_for('results'))

    @app.route('/results')
    def results():
        parameters = {'valves_number': NUMBER_OF_VALVES}
        results = analyzeUseCase.get_results()
        return render_template('results.html', page='results', results=results, parameters=parameters)

    @app.route('/analyze_progress', methods=['GET'])
    def analyze_progress():
        return json.dumps(analyzeUseCase.get_analyze_progress())

    @app.route('/get_all_images', methods=['POST'])
    def get_all_images():
        zip_file, headers = analyzeUseCase.get_all_images()
        return Response(zip_file, headers=headers)

    @app.route('/get_xlsx_results', methods=['POST'])
    def get_xlsx_results():
        xlsx_file, headers = analyzeUseCase.get_xlsx_results()
        return Response(xlsx_file, headers=headers)

    @app.route('/save_new_analyze_date', methods=['POST'])
    @app.route('/save_new_analyze_date/<string:newDate>', methods=['POST'])
    def save_new_analyze_date(newDate=None):
        return analyzeUseCase.save_new_analyze_date(newDate)
