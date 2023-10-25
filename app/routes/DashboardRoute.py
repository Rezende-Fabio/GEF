from ..controllers.ControllerDashboard import ControllerDashboard
from ..controllers.ControllerConsultas import consultaAtraso
from flask import Blueprint, g

dashboardBlue = Blueprint("dashboardBlue", __name__)

controlerDash = ControllerDashboard()

@dashboardBlue.before_request
def before_request():
    g.qtdeAtraso = consultaAtraso()

dashboardBlue.add_url_rule("/dashboard", "dashboard", controlerDash.renderizaDash, "", methods=["GET"])
dashboardBlue.add_url_rule("/troca-filial", "trocaFilial", controlerDash.trocaFilial, "", methods=["GET"])