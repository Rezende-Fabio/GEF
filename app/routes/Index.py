from flask import render_template, request, redirect, session, jsonify, Blueprint, g
from sqlalchemy import func, text
from ..models.Models import *
from dateutil.relativedelta import relativedelta
from ..extensions.EnviarEmail import EnviaEmail
import random
from calendar import monthrange
from werkzeug.security import generate_password_hash
from datetime import datetime
from ..extensions.Log import Log
import sys
from ..extensions.veriaveis import *
from ..configurations.DataBase import DB
from flask_login import login_required


###################################
# Rotas relacionadas ao Index
###################################

indexBlue = Blueprint("indexBlue", __name__)


#Rota inicial
@indexBlue.route("/")
@indexBlue.route("/index")
def index():
    """
    Função que verifica se máquina que solicitou acesso pode acessar o sistema e rediciona
    para o index.
    
    PARAMETROS:
      request.remote_addr = IP da máquina que solicitou acesso no sistema.
    
    RETORNOS:
      return render_template("alert.html") = Caso a máquina não tem direito redireciona 
        para uma tela de erro;
      return f"{BASEDIR}/app/" = Caso a máquina tenha direito redireciona para o index.
    """
    
    #Verificação dos ips que tem acesso ao sistema
    with open(f"{get_path_variaveis()}Ips.txt", "r+") as txt:
        ips = txt.read()

    result = DB.session.execute(text("PRAGMA database_list;")).fetchall()
    base = result[0][2]
    if "GefIII_teste.db" in base:
        session["base"] = "TESTE"
    else:
        session["base"] = "PRODUCAO"
    
    if request.remote_addr not in ips:
        return render_template("public/alert.html")
    else:
        return render_template("public/index.html")
    

#Rota para esqueci a senha 
@indexBlue.route("/esqueci-senha", methods=["GET", "POST"])
def esqueciSenha():
    ###################################################################################################
    #   Função que procura no banco de dados usuário correspondente ao usuário e e-mail digitado.
    #   Se existir ele gera uma senha temporária e envia no e-mail, e muda o campo s_novaSenha 
    # para 1 (ao logar no sistema esse campo estiver 1, será exibida uma tela para alterção
    # de senha).
    #   Se não existir ele retorna um aviso para o usuário.
    
    # PARAMETROS:
    #   request.form["email"] = E-mail digitado no input do modal;
    #   request.form["usuario"] = Usuário digitado no input do modal.
    
    # RETORNOS:
    #   return jsonify({"success": True}) = Retorna Json True quando o e-mail é enviado com sucesso;
    #   return jsonify({"success": False, "email": "Error"}) = Retorna Json Flase e Error quando
    #     não é possivel enviar o e-mail;
    #   return jsonify({"success": False}) = Retorna Json quando o usuário e o e-mail não existem 
    #     no banco;
    #   return render_template("index.html", context=context) = Redireciona para o index do 
    #     sistema pasando context com as veriáveis para utilizar no template.
    ###################################################################################################
    
    if request.method == "POST":
        email = request.form["email"] 
        user = request.form["usuario"].upper()
        conexao = SysUsers #Conexão com a tabela de usuário
        usuario = conexao.query.filter_by(s_usuario=f"{user}", s_email=f"{email}").first() #Query trazendo o usuário correspondente ao usuário e e-mail
        if usuario:
            senha = []
            for x in range(0,5): #Gera senha com 5 números aleatórios
                senha.append(random.randint(0, 9))
                
            senha = "".join(map(str, senha)) #Transforma a lista em string
            usuario.s_senha = generate_password_hash(senha) #Gera hash da senha temporária e grava no banco
            usuario.s_novaSenha = 1 #Grava 1 no banco, para mostrar modal de mudaça de senha no proximo login
            DB.session.commit()
            
            respEmail = EnviaEmail.enviarEmail(email, senha) #Função para enviar e-mail com a senha temporária
            
            if respEmail: #Verifica o retorno da função enviar e-mail
                return jsonify({"success": True})
            else:
                return jsonify({"success": False, "email": "Error"})
            
        else:
            return jsonify({"success": False})
    
    context = {"aviso": 1} #Dicionário contendo as variáveis utilizadas no template 
    return render_template("public/index.html", context=context) #Retorna passando aviso = 1 para mostral modal no template
        
#Rota para a atualização da senha ao entrar no sistema
@indexBlue.route("/cad-senha/<id>", methods=["GET", "POST"])
@login_required
def cadastraNovaSenha(id):
    ###################################################################################################
    # Função que recebe a nova senha do usuário e garva no banco.
    
    # PARAMETROS:
    #   id = Id do usuario que solicitou a troca da senha.
    
    # RETORNOS:
    #   return redirect("/base") = Redireciona para o menu do sistema;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if request.method == "POST":
            conexao = SysUsers #Conexão com a tabela de usuário
            usuario = conexao.query.get(id) #Query trazendo o usuário de acordo com o id passado
            usuario.s_senha = generate_password_hash(request.form["senha"].upper()) #Gera o hash para gravar a nova senha no banco 
            usuario.s_novaSenha = 0 #Muda o status para zero novamente
            DB.session.commit()
            return redirect("/base")
        
    except Exception as erro:
        log = Log()
        log.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/error_500") 