from flask import Blueprint, g
from ..controllers.ControllerConsultas import consultaAtraso
from ..controllers.ControllerEstorno import ControllerEstorno

###################################
# Rotas relacionadas aos movimentos
# TABELA DE MOVIMENTOS GF3006
###################################

estornoBlue = Blueprint("estornoBlue", __name__, url_prefix="/estorno")
controleEstorno = ControllerEstorno()

@estornoBlue.before_request
def before_request():
    g.qtdeAtraso = consultaAtraso()


estornoBlue.add_url_rule("/lista-estorno", "renderListaEstorno", controleEstorno.renderListaEstorno, "", methods=["GET"])
estornoBlue.add_url_rule("/estornos", "consultarBaixasParaEstornos", controleEstorno.consultarBaixasParaEstornos, "", methods=["GET"])
estornoBlue.add_url_rule("/<int:doc>/<int:parcela>", "renderConsultarBaixasParaEstorno", controleEstorno.renderConsultarBaixasParaEstorno, "", methods=["GET"])
estornoBlue.add_url_rule("/estornar-baixa", "estornarBaixa", controleEstorno.estornarBaixa, "", methods=["PUT"])
