from flask import render_template, request, redirect, flash, session, jsonify, Blueprint, g
from sqlalchemy import func
from ..models.Models import *
from ..extensions.integracao import *
from datetime import datetime
from ..extensions.Log import Log
from ..extensions.configHtml import *
import sys
from ..extensions.veriaveis import *
from dateutil.relativedelta import relativedelta
from ..configurations.DataBase import DB
from flask_login import login_required


###################################
# Rotas relacionadas aos movimentos
# TABELA DE MOVIMENTOS GF3006
###################################

estornoBlue = Blueprint("estornoBlue", __name__)

@estornoBlue.before_request
def before_request():
    conexao = Gf3004
    dataAtual = datetime.today().strftime("%Y%m%d") 
    qtdeAtraso = conexao.query.filter(conexao.t_dataVenc<dataAtual, conexao.t_ativo==True, conexao.t_status==True).count()
    
    g.qtdeAtraso = qtdeAtraso


#Rota para tela de listagem de titulos para baixar
@estornoBlue.route("/lista-estorno", methods=["GET", "POST"])
@login_required
def listaEstorno():
    ###################################################################################################
    # Função que renderiza a tela de listagem de baixas.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("baixa/listaBaixas.html") = Redireciona para listagem de baixas;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        context = {"active": "estorno", "titulo": "Lista de Estornos"}
        return render_template("estorno/listaEstorno.html", context=context)
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro)
        return redirect("/")  

#Rota para modal de confirmação de cancelamento da baixa   
@estornoBlue.route("/deletar-baixa/<doc>/<parcela>")
@login_required
def popupDelBaixa(doc, parcela):
    ###################################################################################################
    # Função que renderiza a tela de listagem de baixas.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("baixa/listaBaixas.html") = Redireciona para listagem de baixas;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        conexao5 = Gf3006
        baixas = conexao5.query.filter(conexao5.m_numDoc == doc, conexao5.m_parcela == parcela, conexao5.m_ativo == 1)
        context = {"baixas": baixas, "aviso": 1}
        return render_template("estorno/listaEstorno.html", context=context)
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro)
        return redirect("/")
    
#Rota para estornar as baixas    
@estornoBlue.route("/deletar-baixa", methods=["GET", "POST"])
@login_required
def deletarBaixa():
    ###################################################################################################
    # Função que renderiza a tela de listagem de baixas.
    
    # PARAMETROS:Gf3004
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("baixa/listaBaixas.html") = Redireciona para listagem de baixas;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if request.method == "POST":
            listaIds = request.get_json(force=True)
            ids = []
            conexao = Gf3006
            conexao2 = Gf3004
            conexao3 = Gf3005
            conexao4 = Gf3007
            for id in listaIds["list"]:
                ids.estornoBlueend(id)
                
                baixa = conexao.query.filter_by(m_id=id).first()
                baixa.m_ativo = 0
                
                devolucao = conexao4.query.filter_by(d_id=baixa.m_idDev).first()
                
                if devolucao:
                    devolucao.estornaCredito(baixa.m_valor)
                else:
                    comissao = conexao3.query.filter_by(c_idBaixa=id).first()
                    comissao.c_ativo = 0
                
                titulo = conexao2.query.filter_by(t_numDoc=baixa.m_numDoc, t_numParcela=baixa.m_parcela).first()
                titulo.estornaSaldo(baixa.m_valor)
            
                DB.session.commit()
                Logger.log("Estorno de Baixa", session["usuario"], session["filial"], f"Documento: {baixa.m_numDoc} Parcela: {baixa.m_parcela}")
            return jsonify({"success": True, "ids":ids})
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro)
        return redirect("/")
    

#Rota para preencher a lista de baixas
@estornoBlue.route("/estornos", methods=["GET", "POST"])
@login_required
def estornos():
    ###################################################################################################
    # Função que renderiza a tela de listagem de baixas.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return jsonify(lista) = Retorna Json com lista de títulos com baixas;
    #   return jsonify("Error") = Retorna Json com erro caso aconteça exeção.
    ###################################################################################################
    
    try:
        if request.method == "POST":
            conexao = Gf3004 #Conexão com a tabela de títulos
            conexao2 = Gf3003 #Conexão com a tabela de segmentos 
            conexao3 = Gf3001 #Conexão com a tabela de clientes
            conexao4 = Gf3002 #Conexão com a tabela de vendedores
            
            dataAtual = datetime.now()
            dataAtual = dataAtual - relativedelta(years=leAnoEstorno())
            dataAtual = dataAtual.strftime("%Y")
            #Query que trás todos os títulos que estão baixados
            estornos = DB.session.query(conexao.t_docRef, conexao.t_numDoc, conexao.t_numParcela, conexao.t_idCliente, conexao.t_idVendedor, conexao.t_dataLanc, conexao.t_dataVenc, conexao.t_status, conexao.t_saldo, conexao2.s_abrev, conexao3.c_razaosocial.label("cliente"), conexao4.v_nome.label("vendedor")).filter(conexao.t_ativo == 1, conexao.t_saldo != conexao.t_valor, conexao.t_dataLanc >= dataAtual).join(conexao2, conexao2.s_id == conexao.t_segmento).join(conexao3, conexao.t_idCliente==conexao3.c_id).join(conexao4, conexao.t_idVendedor==conexao4.v_id).order_by(conexao.t_dataVenc)
            
            lista = []
            for x in estornos:
                lista.append({"ref": x.s_abrev + x.t_docRef, "doc": x.t_numDoc, "par": x.t_numParcela, "cli": filtroNome(x.cliente), "vend": filtroNome(x.vendedor), "lanc": filtroData(x.t_dataLanc), "venc":filtroData(x.t_dataVenc)})
            
            return jsonify(lista)
            
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return jsonify("Error")
 