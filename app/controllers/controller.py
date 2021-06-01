from flask import render_template
from app.domain.models.webcam import Webcam
from app.domain.use_cases.webcam_use_case import WebcamUseCase
from app.domain.use_cases.analyze_use_case import AnalyzeUseCase
from app.controllers import home_controller, analyze_controller


def configure_routes(app):
    """ Ocorrem as instanciações das classes principais e chamam-se os controladores específicos das rotas. 

    As classes principais são a 'Webcam' e a 'Analyze'.
    Define-se também a rota de erro da aplicação, usada em ambos os casos.
    """

    @app.route('/error')
    def error():
        return render_template('error.html', page='error')

    webcam = Webcam()
    webcamUseCase = WebcamUseCase(webcam)
    analyzeUseCase = AnalyzeUseCase(webcam)
    home_controller.configure_routes(app, webcamUseCase)
    analyze_controller.configure_routes(app, analyzeUseCase)
