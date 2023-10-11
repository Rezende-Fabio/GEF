from ..controllers.ControllerLogin import ControllerLogin
from flask_login import login_required
from flask import request, Blueprint


autenticacaoBlue = Blueprint("autenticacaoBlue", __name__)


#Rota para autenticação no sistema
@autenticacaoBlue.route("/autenticar", methods=["POST"])
def autenticar():
    ###################################################################################################
    # Função que verifica se o usário existe no banco e faz a autenticação do mesmo no sistema.
    
    # PARAMETROS:
    #   request.form["usuario"] = Usuário que foi digitado no input da tela login;
    #   request.form["senha"] = Senha que foi digitada no input da tela login.
    
    # RETORNOS:
    #   return render_template("menu.html", context=context) = Redireciona para o menu do 
    #     sistema pasando context com as veriáveis para utilizar no template;
    #   return redirect("/") = Redireciona para o index.
    ###################################################################################################
    
    controleLogin = ControllerLogin()
    return controleLogin.efetuarLogin(request.form)
    
            
#Rota para fazer logout
@autenticacaoBlue.route("/logout", methods=["GET"])
@login_required
def logout():
    ###################################################################################################
    # Função que zera as variáveis do cookie e faz o logout no sistema.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return redirect("/") = Redireciona para o index.
    ###################################################################################################

    controleLogin = ControllerLogin()
    return controleLogin.efetuarLogout()