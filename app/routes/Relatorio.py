from flask import render_template, request, redirect, flash, session, jsonify, Blueprint, g
from sqlalchemy import func
from ..models.Models import *
from ..extensions.integracao import *
from datetime import datetime
from ..extensions.logs import Logger
import sys
from flask_login import login_required

###################################
# Rotas relacionadas aos relatórios
###################################

relatorioBlue = Blueprint("relatorioBlue", __name__)

@relatorioBlue.before_request
def before_request():
    conexao = Gf3004
    dataAtual = datetime.today().strftime("%Y%m%d") 
    qtdeAtraso = conexao.query.filter(conexao.t_dataVenc<dataAtual, conexao.t_ativo==True, conexao.t_status==True).count()
    
    g.qtdeAtraso = qtdeAtraso

#Rota para a tela de parametros do relatório de comissão
@relatorioBlue.route("/relat-comissao", methods=["GET"])
@login_required
def relatComissao():
    ###################################################################################################
    # Função que redireciona para a tela de parametros da impressão do relatório de comissão.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("relatorios/relatComissao.html") = Redireciona para os parametros de 
    #     impressão do relatório;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        context = {"active": "relatComi", "titulo": "Parâmetros para o relatório de comissão"}
        return render_template("relatorios/relatComissao.html", context=context)

    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera o log passando a URL e o erro
        return redirect("/index")

#Rota para a tela de parametros do relatório de devoluções    
@relatorioBlue.route("/relat-devolucao", methods=["GET"])
@login_required
def relatDevolucao():
    ###################################################################################################
    # Função que redireciona para a tela de parametros da impressão do relatório de devolução.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("relatorios/relatDevolucao.html") = Redireciona para os parametros de 
    #     impressão do relatório;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        context = {"active": "relatDev", "titulo": "Parâmetros para o relatório de devoluções"}
        return render_template("relatorios/relatDevolucao.html", context=context)
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera o log passando a URL e o erro
        return redirect("/index")

#Rota para a tela de parametros do relatório de títulos recebidos    
@relatorioBlue.route("/relat-recebidos", methods=["GET"])
@login_required
def relatRecebidos():
    ###################################################################################################
    # Função que redireciona para a tela de parametros da impressão do relatório de títulos recebidos,
    # passando os segmentos que estão cadastrados no sistema para um dropBox.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("relatorios/relatRecebidos.html", context=context) = Redireciona para 
    #     os parametros de impressão do relatório passando os segmentos;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        conexao = Gf3003
        segmentos = conexao.query.filter()
        context = {"segmentos": segmentos, "active": "relatRecebidos", "titulo": "Parâmetros para o relatório de títulos recebidos"}
        return render_template("relatorios/relatRecebidos.html", context=context)
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera o log passando a URL e o erro
        return redirect("/index")
    
#Rota para a tela de parametros do relatório de títulos a receber
@relatorioBlue.route("/relat-receber", methods=["GET"])
@login_required
def relatReceber():
    ###################################################################################################
    # Função que redireciona para a tela de parametros da impressão do relatório de títulos a receber,
    # passando os segmentos que estão cadastrados no sistema para um dropBox.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("relatorios/relatReceber.html", context=context) = Redireciona para 
    #     os parametros de impressão do relatório passando os segmentos;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        conexao = Gf3003
        segmentos = conexao.query.filter()
        context = {"segmentos": segmentos, "active": "relatReceber", "titulo": "Parâmetros para o relatório de títulos a receber"}
        return render_template("relatorios/relatReceber.html", context=context)
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera o log passando a URL e o erro
        return redirect("/index")
    
#Rota para a tela de parametros do relatório de títulos a receber
@relatorioBlue.route("/relat-consistecia", methods=["GET"])
@login_required
def relatConsistencia():
    ###################################################################################################
    #   Função que redireciona para a tela de parametros da impressão do relatório de consistência.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("relatorios/relatConsistencia.html") = Redireciona para os parametros de 
    #     impressão do relatório;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        context = {"active": "relatConsis", "titulo": "Parâmetros para o relatório de consistência"}
        return render_template("relatorios/relatConsistencia.html", context=context)
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera o log passando a URL e o erro
        return redirect("/index")
    
#Rota para a tela de parametros do relatório de Observações
@relatorioBlue.route("/relat-observacoes", methods=["GET"])
@login_required
def relatObservacoes():
    ###################################################################################################
    #   Função que redireciona para a tela de parametros da impressão do relatório de observações.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("relatorios/relatObservacao.html") = Redireciona para os parametros de 
    #     impressão do relatório;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        context = {"active": "relatObs", "titulo": "Parâmetros para o relatório de observações"}
        return render_template("relatorios/relatObservacao.html", context=context)
    
    except Exception as erro: 
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera o log passando a URL e o erro
        return redirect("/index")