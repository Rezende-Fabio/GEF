from flask import render_template, request, redirect, flash, session, jsonify, Blueprint, g
from sqlalchemy import func
from ..models.Models import *
from datetime import datetime
from ..extensions.Log import Log
from ..extensions.configHtml import *
import sys
from ..configurations.DataBase import DB
from flask_login import login_required

###################################
# Rotas relacionadas aos movimentos
# TABELA DE MOVIMENTOS GF3006
###################################

baixaBlue = Blueprint("baixaBlue", __name__)

@baixaBlue.before_request
def before_request():
    conexao = Gf3004
    dataAtual = datetime.today().strftime("%Y%m%d") 
    qtdeAtraso = conexao.query.filter(conexao.t_dataVenc<dataAtual, conexao.t_ativo==True, conexao.t_status==True).count()
    
    g.qtdeAtraso = qtdeAtraso


#Rota para tela de listagem de titulos para baixar
@baixaBlue.route("/lista-baixas", methods=["GET", "POST"])
@login_required
def listaBaixas():
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
        context = {"active": "baixa", "titulo": "Lista de Baixas"}
        return render_template("baixa/listaBaixas.html", context=context)
    
    except Exception as erro:
        log = Log()
        log.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/error_500")  

#Rota para tela de baixa do título
@baixaBlue.route("/cad-baixa/<doc>/<parcela>", methods=["GET", "POST"])
@login_required
def cadBaixa(doc, parcela):
    ###################################################################################################
    # Função que renderiza a tela de biaxa do título que foi selecionado.
    
    # PARAMETROS:
    #   doc = Número do documento do título que foi selecionado;
    #   parcela = Número da parcela do título que foi selecionado.
    
    # RETORNOS:
    #   return render_template("baixa/cadBaixa.html", context=context)  = Redireciona para baixa do 
    #     título com os dados referentes ao título que foi seleiconado;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        conexao = Gf3004 #Conexão com a tabela de títulos
        conexao2 = Gf3003 #Conexão com a tabela de segmentos 
        conexao3 = Gf3001 #Conexão com a tabela de clientes
        conexao4 = Gf3002 #Conexão com a tabela de vendedores
        conexao5 = Gf3007 #Conexão com a tabela de devolução
        #Query que trás o título de acordo com o número do documento e parcela passado
        titulo = conexao.query.filter_by(t_numDoc=doc, t_numParcela=parcela).first()
        #Query que trás o segmento, cliente e o vendedor do título
        segCliVend = DB.session.query(conexao.t_idCliente, conexao.t_idVendedor, func.count(conexao.t_numParcela).label('parcelas'), conexao.t_valor, conexao2.s_abrev, conexao2.s_id, conexao3.c_razaosocial, conexao4.v_nome).filter(conexao.t_ativo == 1, conexao.t_numDoc == doc).join(conexao2, conexao2.s_id == conexao.t_idSegmento).join(conexao3, conexao3.c_id == conexao.t_idCliente).join(conexao4, conexao4.v_id == conexao.t_idVendedor).group_by(conexao.t_idCliente, conexao.t_idVendedor, conexao2.s_abrev)
        #Query que trás o número de parcelas do título
        parcelas = DB.session.query(conexao.t_dataVenc, conexao.t_valor, conexao.t_numParcela).filter(conexao.t_numDoc == doc).order_by(conexao.t_numParcela)
        #Query que trás o crédito do cliente caso ele tenha
        credito = DB.session.query(conexao5.d_id).filter(conexao5.d_idCliente==titulo.t_idCliente, conexao5.d_status==1, conexao5.d_ativo==1).join(conexao, conexao.t_idCliente == conexao5.d_idCliente).count()
        context = {"tituloDoc": titulo, "segCliVend": segCliVend, "parcelas": parcelas, "credito": credito, "active": "baixa", "titulo": "Baixa do Título"} #Dicionário contendo as variáveis para utilizar no template
        return render_template("baixa/cadBaixa.html", context=context)     
        
    except Exception as erro:
        log = Log()
        log.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/error_500")

#Rota para inserir baixa do titulo        
@baixaBlue.route("/insert-baixa", methods=["GET", "POST"])
@login_required
def insertBaixa():
    ###################################################################################################
    # Função que verifica se foi uma baixa parcial, baixa total, devolução total ou devolução parcial
    # e insere a baixa no banco.
    
    # PARAMETROS:
    #   request.form["cliente"] = Cliente do título;
    #   request.form["valorCredito"] = Valor do crédito caso ele tenha;
    #   request.form["idDevolucao"] = Id da devolução que foi selecionada, caso tenha;
    #   request.form["valorSaldo"] = Valor do saldo do título que está na tabela;
    #   request.form["valorParcela"] = Valor da parcela;
    #   request.form["obs"] = Observação que foi informada;
    #   request.form["valorBaixa"] = Valor da baixa que foi informado;
    #   request.form["juros"] = Valor do juros que foi informado;
    #   request.form["desconto"] = Valor do desconto que foi informado;
    #   request.form["numDoc"] = Número do documento do título;
    #   request.form["parcela"] = Número da parcela do título;
    #   request.form["dataBaixa"] = Data da baixa que foi informada;
    #   request.form["docRef"] = Número do documento de refência do título;
    #   request.form["filial"] = Filial do título;
    #   request.form["segmento"] = Segmento do título.
    #   request.form["comissao"] = comissão do título.
    
    # RETORNOS:
    #   return redirect("/lista-baixas") = Redireciona para listagem de baixas com a mensagem que baixa
    #     feita com sucesso;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if request.method == "POST":
            
            idCliente = list(request.form["cliente"].split())
            if request.form["valorCredito"] != "":
                idDev = request.form["idDevolucao"]
                juros = 0
                desconto = 0
                
                conexao = Gf3007
                devolucao = conexao.query.filter_by(d_id=idDev).first()
                
                if float(request.form["valorSaldo"]) != float(request.form["valorParcela"]):
                    tipoBaixa = "DP"
                elif devolucao.d_saldo >= float(request.form["valorParcela"]):
                    tipoBaixa = "DT"
                elif devolucao.d_saldo < float(request.form["valorParcela"]):
                    tipoBaixa = "DP"
                
                valorBaixa = devolucao.calculaCredito(float(request.form["valorSaldo"]))
                
                if request.form["obs"] == "":
                    observ = None
                else:
                    observ = request.form["obs"]
                    
            else:
                valorBaixa = float(request.form["valorBaixa"])
                
                if float(request.form["valorBaixa"]) == float(request.form["valorParcela"]):
                    tipoBaixa = "BT"
                else:
                    tipoBaixa = "BP"
                    
                if request.form["juros"] == "" or request.form["juros"] == "0":
                    juros = 0
                else:
                    juros = request.form["juros"]
                    
                if request.form["desconto"] == "" or request.form["desconto"] == "0":
                    desconto = 0
                else: 
                    desconto = request.form["desconto"]
                
                idDev = ""
                
                if request.form["obs"] == "":
                    observ = None
                else:
                    observ = request.form["obs"]
                    
            baixa = Gf3006(
                m_numDoc=request.form["numDoc"],
                m_parcela=request.form["parcela"],
                m_dataBaixa=request.form["dataBaixa"].replace("-", ""),
                m_docRef=request.form["docRef"],
                m_idCliente=idCliente[0],
                m_valor=valorBaixa,
                m_tipoBaixa=tipoBaixa,
                m_filial=request.form["filial"],
                m_juros=float(juros),
                m_deconto=float(desconto),
                m_observ=observ,
                m_usuario=session["usuario"]["usuario"],
                m_idDev=idDev,
                m_idSegmento=request.form["segmento"],
                m_ativo=1
            )

            conexao = Gf3004 #Conexão com a tabela de títulos
            #Query que trás o título de acordo com o número dodocumento e a parcela
            titulo = conexao.query.filter_by(t_numDoc=request.form["numDoc"], t_numParcela=request.form["parcela"]).first()
            titulo.calculaSaldo(valorBaixa) #Calcula o novo saldo do título

            DB.session.add(baixa)
            DB.session.commit()

            if "D" not in tipoBaixa: #Calcula a comisssão caso não seja baixa por devolução
                conexao = Gf3006 #Conexão com a tabela de comissões
                #Query que trás o id da última baixa efetuada
                Baixa = conexao.query.order_by(conexao.m_id.desc()).first()
                
                idVendedor = list(request.form["vendedor"].split())
                comissao = Gf3005(
                    c_idVendedor= idVendedor[0],
                    c_baseCalc=Baixa.calculaBase(),
                    c_idBaixa=Baixa.m_id,
                    c_valor=Baixa.calculaComissao(float(request.form["comissao"])),
                    c_dataBaixa=request.form["dataBaixa"].replace("-", ""),
                    c_dataPgto="",
                    c_docRef=request.form["docRef"],
                    c_numDoc=request.form["numDoc"],
                    c_perc=float(request.form["comissao"]),
                    c_ativo=1
                )
                
                DB.session.add(comissao)
                DB.session.commit()

            flash(f"Baixa efetuada com sucesso!", "success") #Mensagem para ser exibida no Front
            #Logger.log("Baixa de Título", session["usuario"], session["filial"], f"Documento: {request.form['numDoc']} Parcela: {request.form['parcela']}") #Gera log informando que foi feita baixa no título 
            return redirect("/lista-baixas")
        
    except Exception as erro:
        log = Log()
        log.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/error_500")


#Rota para preencher a lista de baixas
@baixaBlue.route("/baixas", methods=["GET", "POST"])
@login_required
def baixas():
    ###################################################################################################
    # API que consulta as baixas para a listagem.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return jsonify(lista) = Retorna Json com a lista de título em baretos para listagem de baixas;
    #   return jsonify("Error") = Retorna Json caso ocorra um erro.
    ###################################################################################################
    
    try:
        if request.method == "POST":
            dataAtual = datetime.today().strftime("%Y%m%d")
            conexao = Gf3004
            conexao2 = Gf3003
            conexao3 = Gf3001
            conexao4 = Gf3002
            #Query que trás todos os títulos que estão em berto 
            baixas = DB.session.query(conexao.t_docRef, conexao.t_numDoc, conexao.t_numParcela, conexao.t_idCliente, conexao.t_idVendedor, conexao.t_dataLanc, conexao.t_dataVenc, conexao.t_status, conexao.t_saldo, conexao2.s_abrev, conexao3.c_razaosocial.label("cliente"), conexao4.v_nome.label("vendedor")).filter(conexao.t_ativo == 1, conexao.t_status==1).join(conexao2, conexao2.s_id == conexao.t_idSegmento).join(conexao3, conexao.t_idCliente==conexao3.c_id).join(conexao4, conexao.t_idVendedor==conexao4.v_id).order_by(conexao.t_dataVenc)
            lista = []
            for x in baixas:
                if x.t_dataVenc < dataAtual:
                    datavenc = f"<span style='color:red; font-weight: bold;'>{filtroData(x.t_dataVenc)}</span>"
                else:
                    datavenc = f"<span>{filtroData(x.t_dataVenc)}</span>"
                    
                lista.append({"ref": x.s_abrev + x.t_docRef, "doc": x.t_numDoc, "par": x.t_numParcela, "cli": filtroNome(x.cliente), "vend": filtroNome(x.vendedor), "lanc": filtroData(x.t_dataLanc), "venc":datavenc, "saldo":filtroValor(x.t_saldo)})
            
            return jsonify(lista)
            
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return jsonify("Error") 
        