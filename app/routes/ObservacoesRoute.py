from flask import render_template, request, redirect, jsonify, Blueprint, g
from ..models.Models import *
from ..extensions.Log import Log
from ..extensions.configHtml import *
from ..configurations.DataBase import DB
from flask_login import login_required
import sys
from datetime import datetime
from ..controllers.ControllerConsultas import consultaAtraso
from ..controllers.ControllerObservacoes import ControllerObservacoes

########################################################
# Rotas relacionadas os Títulos que contem obervações
########################################################

observacaoBlue = Blueprint("observacaoBlue", __name__, url_prefix="/observacao")
controleObservacoes = ControllerObservacoes()

@observacaoBlue.before_request
def before_request():
    g.qtdeAtraso = consultaAtraso()

observacaoBlue.add_url_rule("/lista-observacoes", "renderListaObservacoes", controleObservacoes.renderListaObservacoes, "", methods=["GET"])
observacaoBlue.add_url_rule("/observacoes", "consultarObservacoes", controleObservacoes.consultarObservacoes, "", methods=["GET"])
observacaoBlue.add_url_rule("/<int:doc>/<int:parc>", "consultarObservacao", controleObservacoes.consultarObservacao, "", methods=["GET"])
