from flask import render_template, request, redirect, flash, session, jsonify, Blueprint, url_for
from ..controllers.ControllerManterUsuario import ControllerManterUsuario
from ..models.Tables import *
from werkzeug.security import generate_password_hash
from datetime import datetime
from ..extensions.logs import Logger
from ..extensions.configHtml import *
import sys
from ..configurations.DataBase import DB


###################################
# Rotas relacionadas aos Usuários
# TABELA DE USUARIOS SYSUSERS 
###################################

usuarioBlue = Blueprint("usuarioBlue", __name__, url_prefix="/usuario")


#Rota para Tela de listagem de usuários
@usuarioBlue.route("/lista-usuarios", methods=["GET"])
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
        if session["usuario"]:
            context = {"active": "usuario", "titulo": "Lista de Usuários"}
            return render_template("usuario/listaUsuarios.html", context=context)
        else:
            return redirect("/")
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")
    
#Rota para modal de confirmação para excluir usuário
@usuarioBlue.route("/lista-usuarios/<id>")
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
        if session["usuario"]:
            conexao = SysUsers #Conexão com a tabela de usuários
            #Query que trás o usuário de acordo com o id passado
            usuario = conexao.query.get(id)
            context = {"usuario": usuario, "aviso": 1} #Dicionário contendo as variáveis para utilizar no template
            return render_template("usuario/listaUsuarios.html", context=context)
        
        else:
            return redirect("/")
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")

#Rota para Tela de cadastrode usuário
@usuarioBlue.route("/cad-usuario")
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
        if session["usuario"]:
            context = {"titulo": "Inclusão de Usuário", "action": "/insert-user", "botao": "Gravar", "active": "usuario"} #Dicionário contendo as variáveis para utilizar no template
            return render_template("usuario/cadUsuario.html", context=context)
        
        else:
            return redirect("/")
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")

#Rota para inserir usuário
@usuarioBlue.route("/insert-user", methods=["GET", "POST"])
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
        if session["usuario"]:
            controleManterUsuario = ControllerManterUsuario()
            controleManterUsuario.inserirUsuario(request.form)
            flash(f"Usuário {request.form['usuario'].upper()} incluido com sucesso!", "success") #Mensagem para ser exibida no Front
            Logger.log("Inserção de Usuário", session["usuario"], session["filial"], f"Nome: {request.form['nome']}") #Gera log informando que foi feita uma inserção de usuário
            return redirect(url_for('usuarioBlue.listaUsuarios'))

        else:
            return redirect("/")
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")

#Rota para a edição do usuário
@usuarioBlue.route("/editar-usuario/<id>", methods=["GET", "POST"])
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
        if session["usuario"]:
            conexao = SysUsers #Conexão com a tabela de usuários
            usuario = conexao.query.get(id)
            if request.method == "POST":
                controleManterUsuario = ControllerManterUsuario()
                controleManterUsuario.editarUsuario(request.form, int(id))
                flash(f"Usuário {request.form['usuario'].upper()} atualizado com sucesso!", "success") #Mensagem para ser exibida no Front
                Logger.log("Alteração de Usuário", session["usuario"], session["filial"], f"ID: {id}") #Gera log informando que foi feita alteração no usuário
                return redirect(url_for('usuarioBlue.listaUsuarios'))

            context = {"titulo": "Atualização de Usuário", "action": "/editar-usuario/", "botao": "Alterar", "usuario": usuario} #Dicionário contendo as variáveis para utilizar no template
            return render_template("usuario/cadUsuario.html", context=context)
        
        else:
            return redirect("/")
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")

#Rota para a exclusão lógica do usuário
@usuarioBlue.route("/deletar-usuario/<id>")
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
        if session["usuario"]:
            conexao = SysUsers
            usuario = conexao.query.get(id)
            usuario.s_ativo = 0
            DB.session.commit()
            flash(f"Usuário {usuario.s_nome} excluido com sucesso!") #Mensagem para ser exibida no Front
            Logger.log("Exclusão de Usuário", session["usuario"], session["filial"], f"ID: {id}") #Gera log informando que foi feita exclusão do usuário
            return redirect("/lista-usuarios")

        else:
            return redirect("/")
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")
    
    
@usuarioBlue.route("/usuarios", methods=["GET", "POST"])
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
        if session["usuario"]:
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