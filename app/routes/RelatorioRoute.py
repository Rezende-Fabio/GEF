from ..controllers.ControllerReletorio import ControllerRelatorio
from ..controllers.ControllerConsultas import consultaAtraso
from flask import Blueprint, g


relatorioBlue = Blueprint("relatorioBlue", __name__, url_prefix="/relatorio")
controleRelatorio = ControllerRelatorio()

@relatorioBlue.before_request
def before_request():
    g.qtdeAtraso = consultaAtraso()

relatorioBlue.add_url_rule("/comissao", "renderRelatComissao", controleRelatorio.renderRelatComissao, "", methods=["GET"])
relatorioBlue.add_url_rule("/devolucao", "renderRelatDevolucao", controleRelatorio.renderRelatDevolucao, "", methods=["GET"])
relatorioBlue.add_url_rule("/recebidos", "renderRelatRecebidos", controleRelatorio.renderRelatRecebidos, "", methods=["GET"])
relatorioBlue.add_url_rule("/receber", "renderRelatReceber", controleRelatorio.renderRelatReceber, "", methods=["GET"])
relatorioBlue.add_url_rule("/consistecia", "renderRelatConsistencia", controleRelatorio.renderRelatConsistencia, "", methods=["GET"])
relatorioBlue.add_url_rule("/observacoes", "renderRelatObservacao", controleRelatorio.renderRelatObservacao, "", methods=["GET"])
