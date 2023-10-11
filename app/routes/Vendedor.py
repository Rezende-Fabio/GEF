from flask import render_template, request, redirect, flash, session, jsonify, Blueprint
from ..models.Tables import *
from ..bd.integracao import *
from datetime import datetime
from ..extensions.logs import Logger
from ..extensions.configHtml import *
import sys

###################################
# Rotas relacionadas aos vendedores
# TABELA DE VENDEDORES GF3002
###################################

vendedorBlue = Blueprint("vendedorBlue", __name__)

#Rota para a tela listagem de vendedores
@vendedorBlue.route("/lista-vendedores", methods=["GET", "POST"])
def listaVendedores():
    ###################################################################################################
    # Função que renderiza a tela de listagem de vendedores.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("vendedor/listaVendedores.html") = Redireciona para listagem de vendedores;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario"]:
            context = {"active": "usuario", "titulo": "Lista de Cliente"}
            return render_template("vendedor/listaVendedores.html", context=context)
            
        else:
            return redirect("/")

    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")
    
#Rota para modal de visualização do vendedor
@vendedorBlue.route("/lista-vendedores/<id>")
def popupViewVend(id):
    ###################################################################################################
    # Função que renderiza a tela de listagem de vendedores com um modal, com os dados do vendedor.
    
    # PARAMETROS:
    #   id = Id do vendedor que foi selecionado.
    
    # RETORNOS:
    #   return render_template("vendedor/listaVendedores.html", context=context) = Redireciona para 
    #     listagem de vendedores com modal, com as informações do vendedor;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario"]:
            conexao = Gf3002 #Conexão com a tabela de vendedores
            #Query que trás o usuário que foi selcionado
            vendedor = conexao.query.get(id)
            context = {"aviso": 2, "vendedor": vendedor} #Dicionário contendo as variáveis para utilizar no template
            return render_template("vendedor/listaVendedores.html", context=context)

        else:
            return redirect("/")

    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")

#Rota para modal de confrimação da atulização da base
@vendedorBlue.route("/atualiza-baseVend-modal")
def popupAtualizaBaseVend():
    ###################################################################################################
    # Função que renderiza a tela de listagem de vendedores com modal para confirmação para a atualização
    # da base(vai buscar os vendedores no Protheus).
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("vendedor/listaVendedores.html", context=context) = Redireciona para 
    #     listagem de vendedores com modal para confrimação para a atualização de base;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario"]:
            context = {"aviso": 1} #Dicionário contendo as variáveis para utilizar no template
            return render_template("vendedor/listaVendedores.html", context=context)

        else:
            return redirect("/")

    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")

#Rota para a atualização da base
@vendedorBlue.route("/atualiza-baseVend", methods=["GET", "POST"])
def atualizaBaseVend():
    ###################################################################################################
    # API que chama a atualização da base de vendedores.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return jsonify("Sucsses") = Retorna Json com sucesso;
    #   return jsonify("Error") = Retorna Json com erro.
    ###################################################################################################
    
    try:
        if session["usuario"]:
            if request.method == "POST":
                Atualizacao.integraVendedor() #Chama função para a atualização
                flash("Base atualizada com sucesso!") #Mensagem para ser exibida no Front
                Logger.log("Atualização da base Vendedores", session["usuario"], session["filial"]) #Gera log informando que foi feita atualização da base de vendedores
            return jsonify("Sucsses")

    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return jsonify("Error")
    
#Rota para autocomplete na tala de cadastro de titulos e de parametros para relatorios
@vendedorBlue.route("/vendedores/<nome>")
def vendedoresInput(nome):
    ###################################################################################################
    # Função que preenche lista do autocomplete na tela de cadastro de títulos e de parametros para 
    # relatorios.
    
    # PARAMETROS:
    #   nome = Nome do vendedor ou id que foi informado.
    
    # RETORNOS:
    #   return jsonify(lista) = Retorna Json com lista dos nomes que foi encontrados no banco;
    #   return jsonify("Error") = Retorna Json com erro.
    ###################################################################################################
    
    try:
        if session["usuario"]:
            conexao = Gf3002 #Conexão com a tabela de vendedores
            if nome.isdigit(): #Verifica se o que foi enviado é número
                #Query que consulta os nomes de acordo com o código do vendedor
                vendedores = conexao.query.filter(conexao.v_id.like(f"%{nome}%"), conexao.v_ativo==1)
            else:
                #Query que consulta os nomes de acordo com o nome do vendedor
                vendedores = conexao.query.filter(conexao.v_nome.like(f"%{nome}%"), conexao.v_ativo==1) 
            lista = [v.as_dict() for v in vendedores]
            return jsonify(lista)
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return jsonify("Error")

#Rota para listagem de vendedores
@vendedorBlue.route("/vendedores", methods=["GET", "POST"])
def vendedores():
    ###################################################################################################
    # API que consulta os vendedores para a listagem.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return jsonify(lista) = Retorna Json com a lista de títulos;
    #   return jsonify("Error") = Retorna Json caso ocorra um erro.
    ###################################################################################################
    
    try:
        if session["usuario"]:
            if request.method == "POST":
                conexao = Gf3002 #Conexão com a tabela de vendedores
                #Query que trás todos os vendedores
                vendedores = conexao.query.order_by(conexao.v_id)
                lista = []
                for x in vendedores:
                  lista.vendedorBlueend({"cod": x.v_id, "nome": x.v_nome, "cpfCnpj": filtroCpf(x.v_cpfcnpj), "tel": x.v_telefone, "status": filtroStatus(x.v_ativo)})  
                return jsonify(lista)
             
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return jsonify("Error")

#Api para verificar se o campo de vendedor nos cadastros estão corretos
@vendedorBlue.route("/api-id-vendedor", methods=["GET", "POST"])
def idVendedor():
    ###################################################################################################
    # API que verifica se o vendedor que foi digitado no cadastro está correto.
    
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
                conexao = Gf3002 #Conexão com a tabela de vendedores
                #Query que trás o vendedor de acordo com o código
                vendedor = conexao.query.filter(conexao.v_id==data["id"]).first()
                if vendedor:
                    return jsonify({"resp": True})
                else:
                    return jsonify({"resp": False})
           
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return jsonify("Error")