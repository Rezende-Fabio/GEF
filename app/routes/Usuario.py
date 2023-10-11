from flask import render_template, request, redirect, flash, session, jsonify, Blueprint, url_for, g
from ..controllers.ControllerManterUsuario import ControllerManterUsuario
from ..models.Models import *
from ..extensions.logs import Logger
from ..extensions.configHtml import *
import sys
from ..configurations.DataBase import DB
from flask_login import login_required
from datetime import datetime


###################################
# Rotas relacionadas aos Usuários
# TABELA DE USUARIOS SYSUSERS 
###################################

usuarioBlue = Blueprint("usuarioBlue", __name__, url_prefix="/usuario")

@usuarioBlue.before_request
def before_request():
    conexao = Gf3004
    dataAtual = datetime.today().strftime("%Y%m%d") 
    qtdeAtraso = conexao.query.filter(conexao.t_dataVenc<dataAtual, conexao.t_ativo==True, conexao.t_status==True).count()
    
    g.qtdeAtraso = qtdeAtraso


#Rota para Tela de listagem de usuários
@usuarioBlue.route("/lista-usuarios", methods=["GET"])
@login_required
def listaUsuarios():
    ###################################################################################################
    # Função que renderiza a tela de listagem de usuários.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("usuario/listaUsuarios.html") = Redireciona para listagem de usuários;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        context = {"active": "usuario", "titulo": "Lista de Usuários"}
        return render_template("usuario/listaUsuarios.html", context=context)
      
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")
    
#Rota para modal de confirmação para excluir usuário
@usuarioBlue.route("/usuario/<id>", methods=["GET"])
@login_required
def popupDeleteUser(id):
    ###################################################################################################
    # Função que renderiza a tela de listagem de usuários com modal de confrimação de exclusão.
    
    # PARAMETROS:
    #   id = Id do usuário que foi selecionado.
    
    # RETORNOS:
    #   return render_template("usuario/listaUsuarios.html", context=context) = Redireciona para 
    #     cadastro de usuário;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        conexao = SysUsers #Conexão com a tabela de usuários
        #Query que trás o usuário de acordo com o id passado
        usuario = conexao.query.get(id)
        context = {"msg": f"Desejesa realmente excluir o(a) usuário(a) {usuario.s_usuario}"} #Dicionário contendo as variáveis para utilizar no template
        return jsonify(context)
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")

#Rota para Tela de cadastrode usuário
@usuarioBlue.route("/cad-usuario")
@login_required
def cadUsuario():
    ###################################################################################################
    # Função que renderiza a tela de cadastro de usuários.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("usuario/cadUsuario.html", context=context) = Redireciona para cadastro
    #     de usuários;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        context = {"titulo": "Inclusão de Usuário", "action": "/insert-user", "botao": "Gravar", "active": "usuario"} #Dicionário contendo as variáveis para utilizar no template
        return render_template("usuario/cadUsuario.html", context=context)
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")


#Rota para inserir usuário
@usuarioBlue.route("/insert-user", methods=["GET", "POST"])
@login_required
def insertUsuario():
    ###################################################################################################
    # Função que insere usuário no banco.
    
    # PARAMETROS:
    #   request.form["usuario"] = Usuário que foi informado no input;
    #   request.form["inputSenha"] = Senha que foi informada no input;
    #   request.form["nomecmp"] = Nome que foi informado no input;
    #   request.form["email"] = E-mail que foi informado no input;
    #   request.form["useradmin"] = Indica se o usuário é admin ou não;
    
    # RETORNOS:
    #   return redirect("/lista-usuarios") = Redireciona para listagem de usuários com a mensagem 
    #     usuário cadastrado com sucesso;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try: 
        controleManterUsuario = ControllerManterUsuario()
        return controleManterUsuario.inserirUsuario(request.form)
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")


#Rota para a edição do usuário
@usuarioBlue.route("/editar-usuario/<id>", methods=["GET", "POST"])
@login_required
def editUsuario(id):
    ###################################################################################################
    # Função que renderiza a tela de cadastro com os dados do usuário que foi selecionado.
    
    # PARAMETROS:
    #   request.form["usuario"] = Usuário que foi informado no input;
    #   request.form["inputSenha"] = Senha que foi informada no input;
    #   request.form["nomecmp"] = Nome que foi informado no input;
    #   request.form["email"] = E-mail que foi informado no input;
    #   request.form["useradmin"] = Indica se o usuário é admin ou não;
    
    # RETORNOS:
    #   return redirect("/lista-usuarios") = Redireciona para listagem de usuários com mensagem que 
    #     foi atualizado com sucesso;
    #   return render_template("usuario/cadUsuario.html", context=context) = Redireciona para o 
    #     cadastro com a insformações do usuário que foi selecionado;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        conexao = SysUsers #Conexão com a tabela de usuários
        usuario = conexao.query.get(id)
        if request.method == "POST":
            controleManterUsuario = ControllerManterUsuario()
            return controleManterUsuario.editarUsuario(request.form, int(id))

        context = {"titulo": "Atualização de Usuário", "action": "/editar-usuario/", "botao": "Alterar", "usuario": usuario} #Dicionário contendo as variáveis para utilizar no template
        return render_template("usuario/cadUsuario.html", context=context)
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")

#Rota para a exclusão lógica do usuário
@usuarioBlue.route("/deletar-usuario/<id>", methods=["DELETE"])
@login_required
def deleteUsuario(id):
    ###################################################################################################
    # Função que efetua o delete lógico do usuário no banco.
    
    # PARAMETROS:
    #   id = Id do usuário que foi selcionado.
    
    # RETORNOS:
    #   return redirect("/lista-usuarios") = Redireciona para listagem de usuários com mensagem que foi
    #     excluido com sucesso;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        conexao = SysUsers
        usuario = conexao.query.get(id)
        if usuario.s_usuario == session["usuario"]["usuario"]:
            flash(f"Usuário logado não pode ser excluido!", "danger") #Mensagem para ser exibida no Front
            return jsonify("error")
        elif id == '1':
            flash(f"O usuário ADMIN não pode ser excluido!", "danger") #Mensagem para ser exibida no Front
            return jsonify("error")
        else:
            usuario.s_ativo = 0
            DB.session.commit()
            flash(f"Usuário {usuario.s_usuario} excluido com sucesso!", "success") #Mensagem para ser exibida no Front
            Logger.log("Exclusão de Usuário", session["usuario"], session["filial"], f"ID: {id}") #Gera log informando que foi feita exclusão do usuário
            return jsonify("success")
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")
    
    
@usuarioBlue.route("/usuarios", methods=["GET", "POST"])
@login_required
def usuarios():
    ###################################################################################################
    # API que retorna um json com lista de usuários exceto os excluidos.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   jsonify(lista) = Retorna json com uma lista dos usuários;
    #   return jsonify("Error") = Retrona json com erro caso ocorra exceção.
    ###################################################################################################
    
    try:
        if request.method == "POST":
            conexao = SysUsers #Conexão com a tabela de usuários
            #Query que trás todos os títulos exeto os excluidos
            usuarios = DB.session.query(conexao.id, conexao.s_usuario, conexao.s_nome, conexao.s_admin).filter(conexao.s_ativo==1)
            lista = []
            for x in usuarios:
                lista.append({"cod": x.id, "user": x.s_usuario, "nome": x.s_nome, "admin": filtroStatusUser(x.s_admin)})
            
            return jsonify(lista)
            
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return jsonify("Error")