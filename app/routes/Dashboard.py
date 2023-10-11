from flask import render_template, request, redirect, session, jsonify, Blueprint, g
from sqlalchemy import func, text
from ..models.Models import *
from werkzeug.security import generate_password_hash
from datetime import datetime
from ..extensions.logs import Logger
import sys
from ..extensions.veriaveis import *
from ..configurations.DataBase import DB
from flask_login import login_required
from ..controllers.ControllerDashboard import ControllerDashboard

###################################
# Rotas relacionadas ao Index
###################################

dashboardBlue = Blueprint("dashboardBlue", __name__)

@dashboardBlue.before_request
def before_request():
    conexao = Gf3004
    dataAtual = datetime.today().strftime("%Y%m%d") 
    qtdeAtraso = conexao.query.filter(conexao.t_dataVenc<dataAtual, conexao.t_ativo==True, conexao.t_status==True).count()
    
    g.qtdeAtraso = qtdeAtraso
    

#Rota para Tela inincial
@dashboardBlue.route("/dashboard")
@login_required
def dashboard():
    try:
        controleDashboard = ControllerDashboard()
        return controleDashboard.efetuaCalculos()
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")
    
#Rota para exibir modal de confrimação para troca de filial    
@dashboardBlue.route("/troca-filial")
@login_required
def trocaFilial():
    ###################################################################################################
    # Função que mostra modal para confrimação para a troca de filial.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   render_template("menu.html", context=context) = Redireciona para o menu do sistema
    #     passando o context contendo a variáveis para utilizar no template;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        conexao = Gf3004 #Conexão com a tabela de títulos
        conexao2 = Gf3003 #Conexão com a tabela de segmentos
        #Query para mostrar os ultimos 5 títulos cadatrados
        titulos = DB.session.query(conexao.t_dataLanc, conexao.t_idCliente, conexao.t_idVendedor, conexao.t_numDoc, func.count(conexao.t_numParcela).label('parcelas'), conexao.t_docRef, conexao2.s_abrev).filter(conexao.t_ativo == 1, conexao.t_filial == session["filial"]).join(conexao2, conexao2.s_id == conexao.t_segmento).group_by(conexao.t_dataLanc, conexao.t_idCliente, conexao.t_idVendedor, conexao.t_numDoc, conexao2.s_abrev).order_by(conexao.t_numDoc.desc())
        paginasTi = titulos.paginate(page=1, per_page=5)
        
        conexao3 = Gf3006
        #Query para mostrar os ultimas 5 baixas cadatradas
        baixas = DB.session.query(conexao3.m_docRef, conexao3.m_numDoc, conexao3.m_parcela, conexao3.m_idCliente, conexao3.m_dataBaixa, conexao3.m_valor, conexao3.m_tipoBaixa).filter(conexao3.m_ativo == 1, conexao3.m_filial == session["filial"]).order_by(conexao3.m_id.desc())
        paginasBa = baixas.paginate(page=1, per_page=5)
        
        context = {"aviso": 2, "paginasTi": paginasTi, "paginasBa": paginasBa} #Dicionário contendo as variáveis para utilizar no template
            
        return render_template("public/menu.html", context=context)
      
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")
    
#Rota para troca de filial
@dashboardBlue.route("/filial")
@login_required
def filial():
    ###################################################################################################
    # Função que efetua a troca de filia.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   render_template("menu.html", context=context) = Redireciona para o menu do sistema
    #     passando o context contendo a variáveis para utilizar no template;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["filial"] == 1: #Troca a Filial na sessão do cookie
            session["filial"] = 2
        else: 
            session["filial"] = 1
            
        conexao = Gf3004 #Conexão com a tabela de títulos
        conexao2 = Gf3003 #Conexão com a tabela de segmentos
        #Query para mostrar os ultimos 5 títulos cadatrados
        titulos = DB.session.query(conexao.t_dataLanc, conexao.t_idCliente, conexao.t_idVendedor, conexao.t_numDoc, func.count(conexao.t_numParcela).label('parcelas'), conexao.t_docRef, conexao2.s_abrev).filter(conexao.t_ativo == 1, conexao.t_filial == session["filial"]).join(conexao2, conexao2.s_id == conexao.t_segmento).group_by(conexao.t_dataLanc, conexao.t_idCliente, conexao.t_idVendedor, conexao.t_numDoc, conexao2.s_abrev).order_by(conexao.t_numDoc.desc())
        paginasTi = titulos.paginate(page=1, per_page=5)
        
        conexao3 = Gf3006 #Conexão com a tabela de movimento
        #Query para mostrar os ultimas 5 baixas cadatradas
        baixas = DB.session.query(conexao3.m_docRef, conexao3.m_numDoc, conexao3.m_parcela, conexao3.m_idCliente, conexao3.m_dataBaixa, conexao3.m_valor, conexao3.m_tipoBaixa).filter(conexao3.m_ativo == 1, conexao3.m_filial == session["filial"]).order_by(conexao3.m_id.desc())
        paginasBa = baixas.paginate(page=1, per_page=5)
        
        conexao4 = Gf3002 #Conexão com a tabela de vendedores
        #Query que trás a quantidade de vendedores cadastrados no sistema
        vendedores = conexao4.query.count()
        
        conexao5 = Gf3001 #Conexão com a tabela de clientes
        #Query que trás a quantidade de clientes cadastrados no sistema
        clientes = conexao5.query.count()
        
        #Query que trás a quantidade de títulos cadastrados no sistema
        qtdeTitulos = conexao.query.filter(conexao.t_ativo==1).count() 
        
        context = {"paginasTi": paginasTi, "paginasBa": paginasBa, "qtdeClientes": clientes, "qtdeVendedores": vendedores, "qtdeTitulo": qtdeTitulos} #Dicionário contendo as variáveis para utilizar no template
        
        return render_template("public/menu.html", context=context)
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")