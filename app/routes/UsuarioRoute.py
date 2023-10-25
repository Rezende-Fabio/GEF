from ..controllers.ControllerUsuario import ControllerUsuario
from ..controllers.ControllerConsultas import consultaAtraso
from flask import Blueprint, g

usuarioBlue = Blueprint("usuarioBlue", __name__, url_prefix="/usuario")
controlerUsuario = ControllerUsuario()

@usuarioBlue.before_request
def before_request():
    g.qtdeAtraso = consultaAtraso()

usuarioBlue.add_url_rule("/lista-usuarios", "renderListaUsuarios", controlerUsuario.renderListaUsuarios, "", methods=["GET"])
usuarioBlue.add_url_rule("/cadastrar-usuario", "renderCadastroUsuario", controlerUsuario.renderCadUsuario, "", methods=["GET"])
usuarioBlue.add_url_rule("/editar-usuario/<int:idUser>", "renderEditarUsuario", controlerUsuario.renderEditUsuario, "", methods=["GET"])
usuarioBlue.add_url_rule("/<int:idUser>", "consultarUsuario", controlerUsuario.consultarUsuario, "", methods=["GET"])
usuarioBlue.add_url_rule("/usuarios", "consultarUsuarios", controlerUsuario.consultarUsuarios, "", methods=["GET"])

usuarioBlue.add_url_rule("/cadastrar-usuario", "inserirUsuario", controlerUsuario.inserirUsuario, "", methods=["POST"])
usuarioBlue.add_url_rule("/editar-usuario/<int:idUser>", "editarUsuario", controlerUsuario.editarUsuario, "", methods=["PUT"])
usuarioBlue.add_url_rule("/excluir-usuario/<int:idUser>", "excluirUsuario", controlerUsuario.excluirUsuario, "", methods=["DELETE"])
    