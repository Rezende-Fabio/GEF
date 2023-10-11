from flask import render_template, request, redirect, flash, session, jsonify, Blueprint
from ..models.Tables import *
from ..extensions.logs import Logger
from ..extensions.configHtml import *
import sys
from ..configurations.DataBase import DB

########################################################
# Rotas relacionadas os Títulos que contem obervações
########################################################

observacaoBlue = Blueprint("observacaoBlue", __name__)

#Rota para tela da listagem de Observações
@observacaoBlue.route("/lista-observacoes", methods=["GET", "POST"])
def listaObservacoes():
    ###################################################################################################
    # Função que renderiza a tela da listagem de títulos com observação.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("observacoes/listaObservacoes.html") = Redireciona para o listagem de
    #     títulos com obervações;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario"]:
            return render_template("observacoes/listaObservacoes.html")
        
        else:
            return redirect("/")
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera o log passando a URL e o erro
        return redirect("/index")
    

#Rota para preencher a lista de observações
@observacaoBlue.route("/observacoes", methods=["GET", "POST"])
def observacoes():
    ###################################################################################################
    # Função que traz todos os títulos que tem observação, e retorna em uma lista para exibir em uma
    # tabela.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return jsonify(lista) = Retorna Json com a listagem de títulos;
    #   return jsonify("Error") = Retrona Json com erro caso usuário não tenha logado ou se der erro;
    ###################################################################################################
    
    try:
        if session["usuario"]:
            if request.method == "POST":
                conexao = Gf3006
                conexao2 = Gf3001
                
                baixas = DB.session.query(conexao.m_numDoc, conexao.m_observ, conexao.m_parcela, conexao.m_dataBaixa, conexao.m_valor, conexao.m_docRef, conexao2.c_razaosocial.label("cliente")).join(conexao2, conexao.m_idCliente==conexao2.c_id).filter(conexao.m_observ!=None, conexao.m_ativo==1)
                lista = []
                for x in baixas:  
                    lista.append({"ref": x.m_docRef, "doc": x.m_numDoc, "par": x.m_parcela, "cli": filtroNome(x.cliente), "lanc": filtroData(x.m_dataBaixa), "valor": filtroValor(x.m_valor)})  
                
                return jsonify(lista)
        else:
            return jsonify("Error")
            
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera o log passando a URL e o erro
        return jsonify("Error")
    
#Rota para modal de visualização dos dados das baixas com Observação
@observacaoBlue.route("/lista-observacoes/view/<doc>/<parc>")
def viewObservacoes(doc, parc):
    ###################################################################################################
    # Função que exibe um Modal com informações do título que foi selecionado.
    
    # PARAMETROS:
    #   doc = Documento do título;
    #   parc = Parcela do título.
    
    # RETORNOS:
    #   return render_template("observacoes/listaObservacoes.html", context=context) = Redireciona
    #      para tela de listagem com um Modal, com a insformações do título;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario"]:
            conexao = Gf3006
            conexao2 = Gf3001
            
            baixa = DB.session.query(conexao.m_numDoc, conexao.m_docRef, conexao.m_parcela, conexao.m_dataBaixa, conexao.m_valor, conexao.m_juros, conexao.m_deconto, conexao.m_tipoBaixa, conexao.m_observ, conexao2.c_razaosocial.label("cliente"), conexao.m_idCliente).join(conexao2, conexao.m_idCliente==conexao2.c_id).filter(conexao.m_numDoc==doc, conexao.m_parcela==parc, conexao.m_observ!=None).first()
            
            context = {"baixa": baixa, "aviso": 1}  #Dicionário contendo as variáveis para utilizar no template
            
            return render_template("observacoes/listaObservacoes.html", context=context) 
        else:
            return redirect("/")
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera o log passando a URL e o erro
        return redirect("/index")