from flask import render_template, jsonify, redirect, url_for
from app.configuration import NUMBER_OF_VALVES
from app.domain.use_cases.valves_use_case import ValvesUseCase
from app.domain.models.valves_control import ValvesControl
from app.domain.models.webcam import Webcam
from app.domain.use_cases.webcam_use_case import WebcamUseCase
from app.domain.use_cases.analyze_use_case import AnalyzeUseCase
from app.controllers import home_controller, analyze_controller, valves_controller


def configure_routes(app):
    """ Ocorrem as instanciações das classes principais e chamam-se os controladores específicos das rotas. 

    As classes principais são a 'Webcam' e a 'Analyze'.
    Define-se também a rota de erro da aplicação, usada em ambos os casos.
    """

    @app.errorhandler(400)
    def resource_not_found(error):
        return jsonify(str(error).replace('400 Bad Request: ', '')), 400

    @app.errorhandler(404)
    def internal_server_error(error):
        parameters = {'message': str(error), 'valves_number': NUMBER_OF_VALVES}
        return render_template('error.html', page='error', parameters=parameters), 404

    webcam = Webcam()
    valvesControl = ValvesControl()

    webcamUseCase = WebcamUseCase(webcam)
    valvesUseCase = ValvesUseCase(valvesControl)
    analyzeUseCase = AnalyzeUseCase(webcam)

    home_controller.configure_routes(app, webcamUseCase)
    valves_controller.configure_routes(app, valvesUseCase)
    analyze_controller.configure_routes(app, analyzeUseCase)
