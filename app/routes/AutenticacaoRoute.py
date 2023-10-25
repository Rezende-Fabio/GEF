from flask import Blueprint
from ..controllers.ControllerLogin import ControllerLogin

autenticacaoBlue = Blueprint("autenticacaoBlue", __name__)

controlerLogin = ControllerLogin()

autenticacaoBlue.add_url_rule("/autenticar", "autenticar", controlerLogin.efetuarLogin, "", methods=["POST"])
autenticacaoBlue.add_url_rule("/logout", "logout", controlerLogin.efetuarLogout, "", methods=["GET"])
