from flask import render_template, request, redirect, flash, session, jsonify, Blueprint
from ..models.Tables import *
from ..bd.integracao import *
from datetime import datetime
from ..extensions.logs import Logger
from ..extensions.configHtml import *
import sys
from ..configurations.DataBase import DB

###################################
# Rotas relacionadas aos clientes
# TABELA DE CLIENETES GF3001
###################################

clienteBlue = Blueprint("clienteBlue", __name__)


#Rota para tela de listagem de clientes 
@clienteBlue.route("/lista-clientes/", methods=["GET", "POST"])
def listaClientes():
    ###################################################################################################
    # Função que renderiza a tela de listagem de clientes.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("cliente/listaClientes.html") = Redireciona para listagem de clientes;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario"]:
            context = {"active": "usuario", "titulo": "Lista de Cliente"}
            return render_template("cliente/listaClientes.html", context=context)
        
        else:
            return redirect("/")
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")
    
#Rota para o popup de vizualização de clientes   
@clienteBlue.route("/lista-clientes/<id>")
def popupViewCli(id):
    ###################################################################################################
    # Função que renderiza a tela de listagem de clientes com um modal, com os dados do cliente.
    
    # PARAMETROS:
    #   id = Id do cliente que foi selecionado.
    
    # RETORNOS:
    #   return render_template("cliente/listaClientes.html", context=context) = Redireciona para 
    #     listagem de clientes com modal, com as informações do cliente;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario"]:
            conexao = Gf3001 #Conexão com a tabela de clientes
            #Query que trás o cliente que foi selecionado
            cliente = conexao.query.get(id)
            context = {"aviso": 2, "cliente": cliente} #Dicionário contendo as variáveis para utilizar no template
            return render_template("cliente/listaClientes.html", context=context)

        else:
            return redirect("/")

    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")
         

#Rota para exibir modal de confrimação para a atualização da base
@clienteBlue.route("/atualiza-baseCli-modal")
def popupAtualizaBaseCli():
    ###################################################################################################
    # Função que renderiza a tela de listagem de clientes com modal para confirmação para a atualização
    # da base(vai buscar os clientes no Protheus).
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("cliente/listaClientes.html", context=context) = Redireciona para 
    #     listagem de clientes com modal para confrimação para a atualização de base;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario"]:
            context = {"aviso": 1} #Dicionário contendo as variáveis para utilizar no template
            return render_template("cliente/listaClientes.html", context=context)

        else:
            return redirect("/")

    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")

#Rota para a atualização da base 
@clienteBlue.route("/atualiza-baseCli", methods=["GET", "POST"])
def atualizaBaseCli():
    ###################################################################################################
    # API que chama a atualização da base de clientes.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return jsonify("Sucsses") = Retorna Json com sucesso;
    #   return jsonify("Error") = Retorna Json com erro.
    ###################################################################################################
    
    try:
        if session["usuario"]:
            if request.method == "POST":
                Atualizacao.integraClientes() #Chama função para a atualização
                flash("Base atualizada com sucesso!") #Mensagem para ser exibida no Front
                Logger.log("Atualização da base Clientes", session["usuario"], session["filial"]) #Gera log informando que foi feita atualização da base de clientes
            return jsonify("Sucsses")
            
        else:
            return redirect("/")

    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")
    
#Rota para autocomplete na tala de cadastro de titulos
@clienteBlue.route("/clientes/<nome>")
def clientesInput(nome):
    ###################################################################################################
    # Função que preenche lista do autocomplete na tela de cadastro de títulos e de parametros para 
    # relatorios.
    
    # PARAMETROS:
    #   nome = Nome do cliente ou id que foi informado.
    
    # RETORNOS:
    #   return jsonify(lista) = Retorna Json com lista dos nomes que foi encontrados no banco;
    #   return jsonify("Error") = Retorna Json com erro.
    ###################################################################################################
    
    try:
        if session["usuario"]:
            conexao = Gf3001 #Conexão com a tabela de clientes
            if nome.isdigit(): #Verifica se o que foi enviado é número
                #Query que consulta os nomes de acordo com o código do cliente
                clientes = conexao.query.filter(conexao.c_id.like(f"%{nome}%"), conexao.c_ativo==1)
            else:
                #Query que consulta os nomes de acordo com o nome do cliente
                clientes = conexao.query.filter(conexao.c_razaosocial.like(f"%{nome}%"), conexao.c_ativo==1) 
            lista = [v.as_dict() for v in clientes]
            return jsonify(lista)
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return jsonify("Error")

#Rota para preencher a lista de clientes
@clienteBlue.route("/clientes", methods=["GET", "POST"])
def clientes():
    ###################################################################################################
    # API que consulta os clientes para a listagem.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return jsonify(lista) = Retorna Json com a lista de títulos;
    #   return jsonify("Error") = Retorna Json caso ocorra um erro.
    ###################################################################################################
    
    try:
        if session["usuario"]:
            if request.method == "POST":
                conexao = Gf3001 #Conexão com a tabela de clientes
                #Query que trás todos os clientes
                clientes = conexao.query.order_by(conexao.c_id)
                lista = []
                for x in clientes:
                  lista.append({"cod": x.c_id, "loja": x.c_loja, "nome": x.c_razaosocial, "cpfCnpj": filtroCpf(x.c_cpfcnpj), "status": filtroStatus(x.c_ativo)})  
                  
                return jsonify(lista)
            
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return jsonify("Error")  
    
#Api para verificar se o campo de cliente nos cadastros estão corretos
@clienteBlue.route("/api-id-cliente", methods=["GET", "POST"])
def idCliente():
    ###################################################################################################
    # API que verifica se o clientes que foi digitado no cadastro está correto.
    
    # PARAMETROS:
    #   data["id"] = Id do vendedor.
    
    # RETORNOS:
    #   return jsonify({"resp": True}) = Retorna Json True;
    #   return jsonify({"resp": False}) = Retorna Json Flase;
    #   return jsonify("Error") = Retorna Json caso ocorra um erro.
    ###################################################################################################
    
    try:
        if session["usuario"]:
            if request.method == "POST":
                data = request.get_json()
                conexao = Gf3001 #Conexão com a tabela de clientes
                #Query que trás o cliente de acordo com o código
                cliente = conexao.query.filter(conexao.c_id==data["id"]).first()
                if cliente:
                    return jsonify({"resp": True})
                else:
                    return jsonify({"resp": False})
            
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return jsonify("Error")