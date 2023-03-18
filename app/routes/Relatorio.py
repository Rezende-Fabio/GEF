from flask import render_template, request, redirect, flash, session, jsonify
from sqlalchemy import func
from app import app
from ..bd.models import *
from datetime import datetime
from ..extensions.logs import Logger
import sys

###################################
# Rotas relacionadas aos relatórios
###################################


#Rota para a tela de parametros do relatório de comissão
@app.route("/relat-comissao")
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
        if session["usuario_logado"]:
            return render_template("relatorios/relatComissao.html")
        
        else:
            return redirect("/")
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera o log passando a URL e o erro
        return redirect("/index")

#Rota para a tela de parametros do relatório de devoluções    
@app.route("/relat-devolucao")
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
        if session["usuario_logado"]:
            return render_template("relatorios/relatDevolucao.html")
        
        else:
            return redirect("/")
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera o log passando a URL e o erro
        return redirect("/index")

#Rota para a tela de parametros do relatório de títulos recebidos    
@app.route("/relat-recebidos")
def relatRecebidos():
    ###################################################################################################
    # Função que redireciona para a tela de parametros da impressão do relatório de títulos recebidos,
    # passando os segmentos que estão cadastrados no sistema para um dropBox.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("relatorios/relatRecebidos.html", contexto=contexto) = Redireciona para 
    #     os parametros de impressão do relatório passando os segmentos;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            conexao = Gf3003
            segmentos = conexao.query.filter()
            contexto = {"segmentos": segmentos}
            return render_template("relatorios/relatRecebidos.html", contexto=contexto)
        
        else:
            return redirect("/")
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera o log passando a URL e o erro
        return redirect("/index")
    
#Rota para a tela de parametros do relatório de títulos a receber
@app.route("/relat-receber")
def relatReceber():
    ###################################################################################################
    # Função que redireciona para a tela de parametros da impressão do relatório de títulos a receber,
    # passando os segmentos que estão cadastrados no sistema para um dropBox.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("relatorios/relatReceber.html", contexto=contexto) = Redireciona para 
    #     os parametros de impressão do relatório passando os segmentos;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            conexao = Gf3003
            segmentos = conexao.query.filter()
            contexto = {"segmentos": segmentos}
            return render_template("relatorios/relatReceber.html", contexto=contexto)
        
        else:
            return redirect("/")
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera o log passando a URL e o erro
        return redirect("/index")
    
#Rota para a tela de parametros do relatório de títulos a receber
@app.route("/relat-consistecia")
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
        if session["usuario_logado"]:
            return render_template("relatorios/relatConsistencia.html")
        
        else:
            return redirect("/")
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera o log passando a URL e o erro
        return redirect("/index")
    
#Rota para a tela de parametros do relatório de Observações
@app.route("/relat-observacoes")
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
        if session["usuario_logado"]:
            return render_template("relatorios/relatObservacao.html")
        
        else:
            return redirect("/")
    
    except Exception as erro: 
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera o log passando a URL e o erro
        return redirect("/index")