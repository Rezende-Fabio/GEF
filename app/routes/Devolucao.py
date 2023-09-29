from flask import render_template, request, redirect, flash, session, jsonify, Blueprint
from ..models.Tables import *
from ..bd.integracao import *
from datetime import datetime
from ..extensions.logs import Logger
from ..extensions.configHtml import *
import sys
from ..configurations.DataBase import DB

###################################
# Rotas relacionadas as devoluções
# TABELA DE DEVOLUÇÂO GF3007
###################################

devolucaoBlue = Blueprint("devolucaoBlue", __name__)


#Rota para tela de cadastro de devolução
@devolucaoBlue.route("/cad-devolucao")
def cadDevolucao():
    ###################################################################################################
    # Função que renderiza a tela de cadastro de devolução.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("devolucao/cadDevolucao.html", contexto=contexto)  = Redireciona para o 
    #     cadastro de devolução;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            data = datetime.today().strftime("%Y-%m-%d") #Data atual
            contexto = {"data": data} #Dicionário contendo as variáveis para utilizar no template
            return render_template("devolucao/cadDevolucao.html", contexto=contexto)
                
        else:
            return redirect("/")
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index") 

#Rota para preencher a lista de devoluções
@devolucaoBlue.route("/devolucoes", methods=["GET", "POST"])
def devolucoes():
    ###################################################################################################
    # API que consulta as devoluções para a listagem.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return jsonify(lista) = Retrona lista de devoluções exceto as excluidas;
    #   return jsonify("Error") = Retorna erro caso aconteça exeção.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            if request.method == "POST":
                conexao = Gf3007 #Conexão com a tabela de devoluções
                conexao2 = Gf3001 #Conexão com a tabela de clientes
                #Query que trás a as devoluções exceto as excluidas
                baixas = DB.session.query(conexao.d_dataCad, conexao.d_id , conexao.d_docRef, conexao.d_valor, conexao2.c_razaosocial.label("cliente")).join(conexao2, conexao2.c_id == conexao.d_idCliente).filter(conexao.d_ativo==1).order_by(conexao.d_dataCad)
                
                lista = []
                for x in baixas:  
                    lista.append({"cli": filtroNome(x.cliente), "valor": filtroValor(x.d_valor), "ref": x.d_docRef, "cad": filtroData(x.d_dataCad), "idDev": x.d_id})  
                
                return jsonify(lista)
            
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return jsonify("Error")
    
#Rota para inserir devolução
@devolucaoBlue.route("/insert-devolucao", methods=["GET", "POST"])
def insertDevolucao():
    ###################################################################################################
    # Função que insere devolução.
    
    # PARAMETROS:
    #   request.form["cliente"] = Id do cliente que foi informado no input;
    #   request.form["valor"] = Valor da devolução que foi informado no input;
    #   request.form["docRef"] = Número do documento de referência qua foi infromado no input;
    #   request.form["dataLanc"] = Data do lançamento da devlução informado no input.
    
    # RETORNOS:
    #   return redirect("/cad-devolucao")  = Redireciona para o cadastro de devolução com mensagem que 
    #     foi cadastrado com sucesso;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            if request.method == "POST":
                idCliente = list(request.form["cliente"].split())
                conexao = Gf3004 #Conexão com a tabela de títulos
                conexao2 = Gf3003 #Conexão com a tabela de segmentos
                #Query que trás o segmento do documento de referência
                segmento = DB.session.query(conexao.t_segmento, conexao2.s_abrev).filter(conexao.t_docRef==int(request.form["docRef"]), conexao.t_idCliente==idCliente[0]).join(conexao2, conexao2.s_id==conexao.t_segmento).group_by(conexao.t_docRef).first()
                
                devolucao = Gf3007(
                    d_idCliente=idCliente[0],
                    d_valor=float(request.form["valor"]),
                    d_docRef=segmento.s_abrev + request.form["docRef"],
                    d_dataCad=request.form["dataLanc"].replace("-", ""),
                    d_saldo=float(request.form["valor"]),
                    d_status=1,
                    d_ativo=1
                )
                DB.session.add(devolucao)
                DB.session.commit()
                
                flash("Devolução cadatrada com sucesso!") #Mensagem para ser exibida no Front
                Logger.log("Devolução", session["usuario_logado"], session["filial"], f"Referência: {request.form['docRef']} Cliente: {idCliente[2]}") #Gera log informando que foi feita inserção da devolução
                return redirect("/cad-devolucao")
                
        else:
            return redirect("/")
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index") 

#Rota para modal de confirmação da exclusão do devolução
@devolucaoBlue.route("/exluir-devolucao-modal/<idDev>", methods=["GET", "POST"])
def excluirDevolucaoModal(idDev):
    ###################################################################################################
    # Função que renderiza a tela de cadastro de devolução com modal de confirmação de exclusão, caso
    # a devolução já foi utilizada retorna mensagem.
    
    # PARAMETROS:
    #   idDev = Id da devolução que foi selecionada;
    
    # RETORNOS:
    #   return redirect("/cad-devolucao") = Redireciona para o cadastro de devolução com mensagem de
    #     alerta;
    #   return render_template("devolucao/cadDevolucao.html",contexto=contexto) = Redireciona para o
    #     cadastro de  devolução com modal de confirmação de exclusão;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            conexao = Gf3006 #Conexão com a tabela de movimento
            #Query que verifica se existe baixas com o id da devolução passado
            existDev = conexao.query.filter(conexao.m_idDev==idDev, conexao.m_ativo==1).first()
            
            if existDev:
                flash("Esta Devolução não pode ser excluida, pois existe(m) baixa(s). Realize o estorno(s) antes da exclusão.") #Mensagem para ser exibida no Front
                return redirect("/cad-devolucao")
            
            else:
                conexao2 = Gf3007 #Conexão com a tabela de devolução
                #Query que trás a devolução de acordo com o id passado
                devolucao = conexao2.query.get(idDev)
                contexto = {"aviso": 1, "devolucao": devolucao} #Dicionário contendo as variáveis para utilizar no template
                return render_template("devolucao/cadDevolucao.html",contexto=contexto)
            
        else:
            return redirect("/")
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index") 
    
#Rota para exclusão da devolução
@devolucaoBlue.route("/exluir-devolucao/<idDev>", methods=["GET", "POST"])
def excluirDevolucao(idDev):
    ###################################################################################################
    # Função que efetua o delete lógico da devolução.
    
    # PARAMETROS:
    #   idDev = Id da devolução que foi selecionada.
    
    # RETORNOS:
    #   return redirect("/cad-devolucao")  = Redireciona para o cadastro de devolução com mensagem que
    #     foi excluido com sucesso;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            conexao2 = Gf3007 #Conexão com a tabela de devolução
            #Query que trás a devolução de acordo com o id passado
            dev = conexao2.query.get(idDev)
            dev.d_ativo = 0
            DB.session.commit()
            
            flash("Crédito excluido com sucesso!") #Mensagem para ser exibida no Front
            Logger.log("Exclusão de Devolução", session["usuario_logado"], session["filial"], f"ID: {idDev}") #Gera log informando que foi feita exclusão da devolução
            return redirect("/cad-devolucao")
            
        else:
            return redirect("/")
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index") 
    
#Rota para verificar se o cliente tem devolução para a baixar o título    
@devolucaoBlue.route("/lista-devolucao-cliente", methods=["GET", "POST"])
def listadevolucaoCliente():
    ###################################################################################################
    # API que consulta as devoluções do cliente na hora da baixa do título.
    
    # PARAMETROS:
    #   idCli["idCli"] = Id do cliente do título.
    
    # RETORNOS:
    #  return jsonify(lista)  = Retorna Json com lista das devoluções do cliente;
    #  return jsonify("Error") = Retorna Json com erro quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            if request.method == "POST":
                conexao = Gf3007
                idCli = request.get_json()
                
                devolucoes = DB.session.query(conexao.d_docRef, conexao.d_saldo, conexao.d_id).filter(conexao.d_idCliente==idCli["idCli"], conexao.d_status==1, conexao.d_ativo==1)
                
                lista = []
                for x in devolucoes:
                    lista.append({"ref": x.d_docRef, "saldo": filtroValor(x.d_saldo), "id": x.d_id})
                
                return jsonify(lista)
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return jsonify("Error") 