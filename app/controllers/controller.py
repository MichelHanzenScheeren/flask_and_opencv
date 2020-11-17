# pylint: disable=unused-variable
from flask import render_template
from app.models.webcam import Webcam
from app.models.analyze import Analyze
from app.controllers import home_controller, analyze_controller


def configure_routes(app):
  """ Ocorrem as instanciações das classes principais da aplicação e chamam-se os controladores específicos das rotas. 

  As classes principais são a 'Webcam' e a 'Analyze'.
  Define-se também a rota de erro da aplicação, usada em ambos os casos.
  """
  
  webcam = Webcam()
  analyze = Analyze()
  home_controller.configure_routes(app, webcam)
  analyze_controller.configure_routes(app, webcam, analyze)

  @app.route('/error')
  def error():
    return render_template('error.html', page='error')
