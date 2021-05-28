# pylint: disable=unused-variable
from flask import render_template, redirect, url_for
from app.models.webcam import Webcam
from app.models.analyze import Analyze
from app.controllers import home_controller, analyze_controller


def configure_routes(app):
    """ Ocorrem as instanciações das classes principais e chamam-se os controladores específicos das rotas. 

    As classes principais são a 'Webcam' e a 'Analyze'.
    Define-se também a rota de erro da aplicação, usada em ambos os casos.
    """

    @app.route('/error')
    def error():
        return render_template('error.html', page='error')

    def redirect_to_error_page():
        return redirect(url_for('error'))

    webcam = Webcam()
    analyze = Analyze()
    home_controller.configure_routes(app, webcam)
    analyze_controller.configure_routes(app, webcam, analyze)
