from ..controllers.ControllerCliente import ControllerCliente
from ..controllers.ControllerConsultas import *
from ..extensions.integracao import Atualizacao
from flask import Blueprint, g

###################################
# Rotas relacionadas aos clientes
# TABELA DE CLIENETES GF3001
###################################

clienteBlue = Blueprint("clienteBlue", __name__, url_prefix="/cliente")
controleCliente = ControllerCliente()

@clienteBlue.before_request
def before_request():
    g.qtdeAtraso = consultaAtraso()
    g.integracao = Atualizacao()
    g.maxCli, g.maxVend = g.integracao.qtdeCliVend()
    

clienteBlue.add_url_rule("/lista-clientes", "renderListaClientes", controleCliente.renderListaClientes, "", methods=["GET"])
clienteBlue.add_url_rule("/<idCli>", "renderConsultarCliente", controleCliente.renderConsultaCliente, "", methods=["GET"])
clienteBlue.add_url_rule("/atualiza-baseCli", "atualizarBaseCliente", controleCliente.atulizarBaseCliente, "", methods=["GET"])
clienteBlue.add_url_rule("/atualiza-baseCli-redirect", "atualizarBaseClienteRedirect", controleCliente.atulizarBaseClienteRedirect, "", methods=["GET"])
clienteBlue.add_url_rule("/clientes/<pesquisa>", "pesquisaAutocomplete", controleCliente.pesquisarClientesAutocomplete, "", methods=["GET"])
clienteBlue.add_url_rule("/clientes", "consultarClientes", controleCliente.consultarClientes, "", methods=["GET"])   
clienteBlue.add_url_rule("/verifica-cliente/<idCli>", "verificarCliente", controleCliente.verificarCliente, "", methods=["GET"])
    