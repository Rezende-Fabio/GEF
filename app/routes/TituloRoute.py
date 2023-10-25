from ..controllers.ControllerConsultas import consultaAtraso
from ..controllers.ControllerTitulo import ControllerTitulo
from flask import Blueprint, g


###################################
# Rotas relacionadas aos titulos
# TABELA DE TITULOS GF3004
###################################

tituloBlue = Blueprint("tituloBlue", __name__, url_prefix="/titulo")
controleTitulo = ControllerTitulo()

@tituloBlue.before_request
def before_request():
    g.qtdeAtraso = consultaAtraso()


tituloBlue.add_url_rule("/lista-titulos", "renderListaTitulos", controleTitulo.renderListaTitulos, "", methods=["GET"])
tituloBlue.add_url_rule("/cadastrar-titulo", "renderCadastrarTitulo", controleTitulo.renderCadastrarTitulo, "", methods=["GET"])
tituloBlue.add_url_rule("/editar-titulo/<int:doc>", "renderEditarTitulo", controleTitulo.renderEditarTitulo, "", methods=["GET"])
tituloBlue.add_url_rule("/view/<int:doc>", "renderConsultarTitulo", controleTitulo.renderConsultarTitulo, "", methods=["GET"])

tituloBlue.add_url_rule("/<int:doc>", "consultarTitulo", controleTitulo.consultarTitulo, "", methods=["GET"])
tituloBlue.add_url_rule("/titulos", "consultarTitulos", controleTitulo.consultarTitulos, "", methods=["GET"])

tituloBlue.add_url_rule("/cadastrar-titulo", "inserirTitulo", controleTitulo.inserirTitulo, "", methods=["POST"])
tituloBlue.add_url_rule("/editar-titulo/<int:doc>", "editarTitulo", controleTitulo.editarTitulo, "", methods=["PUT"])
tituloBlue.add_url_rule("/excluir-titulo/<int:doc>", "excluirTitulo", controleTitulo.excluirTitulo, "", methods=["DELETE"])

tituloBlue.add_url_rule("/doc-ref/<idCli>", "autocompleteIdCliente", controleTitulo.autocompleteIdCliente, "", methods=["GET"])
tituloBlue.add_url_rule("/doc-ref", "verificarDocRefTitulo", controleTitulo.verificarDocRefTitulo, "", methods=["GET"])
tituloBlue.add_url_rule("/doc-ref/<docRef>/<idCli>", "verificaDocRefCliente", controleTitulo.verificaDocRefCliente, "", methods=["GET"])         