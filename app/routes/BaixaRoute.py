from flask import render_template, request, redirect, flash, session, jsonify, Blueprint, g
from sqlalchemy import func
from ..models.Models import *
from datetime import datetime
from ..extensions.Log import Log
from ..extensions.configHtml import *
import sys
from ..configurations.DataBase import DB
from flask_login import login_required
from ..controllers.ControllerConsultas import consultaAtraso
from ..controllers.ControllerBaixa import ControllerBaixa

###################################
# Rotas relacionadas aos movimentos
# TABELA DE MOVIMENTOS GF3006
###################################

baixaBlue = Blueprint("baixaBlue", __name__, url_prefix="/baixa")
controleBaixa = ControllerBaixa()

@baixaBlue.before_request
def before_request():
    g.qtdeAtraso = consultaAtraso()

baixaBlue.add_url_rule("/lista-baixas", "renderListaBaixas", controleBaixa.renderListaBaixas, "", methods=["GET"])
baixaBlue.add_url_rule("/cadastrar-baixa/<int:doc>/<int:parcela>", "renderCadastarBaixa", controleBaixa.renderCadastarBaixa, "", methods=["GET"])
baixaBlue.add_url_rule("/baixas", "consultarBaixas", controleBaixa.consultarBaixas, "", methods=["GET"])
baixaBlue.add_url_rule("/cadastrar-baixa", "inserirBaixa", controleBaixa.inserirBaixa, "", methods=["POST"])
