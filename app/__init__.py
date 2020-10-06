from flask import Flask
from app.controllers import controller


def create_app():
    app = Flask(__name__)
    controller.configure_routes(app)
    return app

