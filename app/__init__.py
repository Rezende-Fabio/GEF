from .configurations import Blueprint
from .configurations import DataBase
from .configurations import Configuration
from flask import Flask

def create_app():
    app = Flask(__name__)

    Configuration.init_app(app)
    DataBase.init_app(app)
    Blueprint.rotas(app)

    return app