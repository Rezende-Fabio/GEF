from .configurations import Blueprint
from .configurations import DataBase
from .configurations import Configuration
from .configurations import FunctionShell
from .configurations import Auth
from flask import Flask

def create_app() -> Flask:
    app = Flask(__name__)

    Configuration.init_app(app)
    DataBase.init_app(app)
    Auth.init_app(app)
    Blueprint.rotas(app)
    FunctionShell.function_shell(app)

    return app