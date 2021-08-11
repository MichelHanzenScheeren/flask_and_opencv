from flask import Flask
from app.controllers import controller


def create_app():
    """ Criação do projeto e configuração das rotas da aplicação. """

    app = Flask(__name__)
    controller.configure_routes(app)
    return app
