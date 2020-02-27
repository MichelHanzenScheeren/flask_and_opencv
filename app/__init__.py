from flask import Flask
from app.controllers import default


def create_app():
    app = Flask(__name__)
    default.configure(app)
    return app

