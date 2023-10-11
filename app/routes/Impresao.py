from flask import render_template, request, redirect, flash, session, jsonify, Blueprint
from sqlalchemy import func, or_
from app.extensions.montaHtmlComi import htmlComissao, htmlComissaoVend
from app.extensions.montaHtmlDev import htmlDevolucao, htmlBaixasDev
from app.extensions.montaHtmlConsis import *
from app.extensions.montaHtmlPlanilha import htmlPlanilha
from app.extensions.montaHtmlObserv import htmlObservacao
from app.extensions.montaHtmlReceber import *
from app.extensions.montaHtmlRecebidos import *
from ..models.Tables import *
from ..bd.integracao import *
from datetime import datetime
from ..extensions.EnviarEmail import *
from ..extensions.logs import Logger
import sys
from ..configurations.DataBase import DB

###################################
# Rotas relacionadas aos relatórios
###################################

impressaoBlue = Blueprint("impressaoBlue", __name__)

############################################################
# Rota para a impressão do relatório de comissões
############################################################
@impressaoBlue.route("/impressao-comissao", methods=["GET", "POST"])
def impreComissao():
    try:
        if session["usuario"]:
            listaVend = []
            dataDe = request.form["dataDe"].replace("-", "")
            dataAte = request.form["dataAte"].replace("-", "")
            if "vendedor" in request.form.keys():
                idVendedor = list(request.form["vendedor"].split())
                nomeVend = ' '.join(map(str, idVendedor[2:]))
                conexao = Gf3005
                conexao2 = Gf3001
                conexao4 = Gf3006
                conexao5 = Gf3003
                
                comissoes = DB.session.query(conexao.c_baseCalc, conexao.c_valor, conexao.c_perc, conexao.c_dataBaixa, conexao.c_docRef, conexao.c_numDoc, conexao4.m_parcela.label("parcela"),
                                                conexao4.m_tipoBaixa.label('tipoBaixa'), conexao2.c_razaosocial.label('cliente'), conexao5.s_abrev.label('segmento')).join(conexao4, conexao4.m_id == conexao.c_idBaixa).join(conexao2, conexao2.c_id == conexao4.m_idCliente).join(conexao5, conexao5.s_id == conexao4.m_segmento).filter(conexao.c_idVendedor==idVendedor[0],
                                                                                                                                                                                                                                                                                                                                        conexao.c_ativo==1, conexao.c_dataBaixa>=dataDe, conexao.c_dataBaixa<=dataAte).order_by(conexao.c_docRef, conexao.c_dataBaixa)
                linhas = DB.session.query(conexao.c_baseCalc, conexao.c_valor, conexao.c_perc, conexao.c_dataBaixa, conexao.c_docRef, conexao.c_numDoc,
                                                conexao4.m_tipoBaixa.label('tipoBaixa'), conexao2.c_razaosocial.label('cliente'), conexao5.s_abrev.label('segmento')).join(conexao4, conexao4.m_id == conexao.c_idBaixa).join(conexao2, conexao2.c_id == conexao4.m_idCliente).join(conexao5, conexao5.s_id == conexao4.m_segmento).filter(conexao.c_idVendedor==idVendedor[0],
                                                                                                                                                                                                                                                                                                                                        conexao.c_ativo==1, conexao.c_dataBaixa>=dataDe, conexao.c_dataBaixa<=dataAte).order_by(conexao.c_docRef, conexao.c_dataBaixa).count()
                                                
                nomeHtml = htmlComissao(comissoes, linhas)
                context = {"datas": [dataDe, dataAte], "vendedor": nomeVend}
                
            else:
                conexao = Gf3005
                conexao2 = Gf3001
                conexao3 = Gf3002
                conexao4 = Gf3006
                conexao5 = Gf3003
                
                vendedores = DB.session.query(conexao.c_idVendedor).distinct(conexao.c_idVendedor).join(conexao3, conexao.c_idVendedor==conexao3.v_id).filter(conexao.c_ativo==1, conexao.c_dataBaixa>=dataDe, conexao.c_dataBaixa<=dataAte).order_by(conexao3.v_nome, conexao.c_docRef, conexao.c_dataBaixa)
                
                for x in vendedores:
                    listaVend.append(x[0])
                
                nomeHtml = htmlComissaoVend(listaVend, dataDe, dataAte)
                context = {"datas": [dataDe, dataAte]}
            
            return render_template(f"impressoes/{nomeHtml}", context=context)
        else:
            return redirect("/")
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro)
        return redirect("/index")
    
############################################################
# Rota para a impressão do relatório de devoluções
############################################################
@impressaoBlue.route("/impressao-devolucao", methods=["GET", "POST"])
def impreDevolucao():
    try:
        if session["usuario"]:
            dataDe = request.form["dataDe"].replace("-", "")
            dataAte = request.form["dataAte"].replace("-", "")
            
            if "cliente" in request.form.keys():
                idCliente = list(request.form["cliente"].split())
                nomeCli = ' '.join(map(str, idCliente[2:]))
                conexao = Gf3007
                davolucoes = DB.session.query(conexao.d_docRef, conexao.d_valor, conexao.d_dataCad, conexao.d_saldo).filter(conexao.d_idCliente==idCliente[0], conexao.d_dataCad>=dataDe, conexao.d_dataCad<=dataAte, conexao.d_ativo==1).order_by(conexao.d_dataCad)
                linhas = DB.session.query(conexao.d_docRef, conexao.d_valor, conexao.d_dataCad, conexao.d_saldo).filter(conexao.d_idCliente==idCliente[0], conexao.d_dataCad>=dataDe, conexao.d_dataCad<=dataAte, conexao.d_ativo==1).order_by(conexao.d_dataCad).count()

                nomeHtml = htmlDevolucao(davolucoes, linhas)
            else:
                conexao = Gf3006
                conexao2 = Gf3001
                conexao3 = Gf3002
                conexao4 = Gf3004
                baixas = DB.session.query(conexao.m_dataBaixa, conexao.m_docRef, conexao.m_numDoc, conexao.m_valor, conexao.m_parcela , 
                                          conexao2.c_razaosocial.label("cliente"), conexao3.v_nome.label("vendedor"), conexao.m_tipoBaixa, 
                                          conexao4.t_saldo.label("saldo")).join(conexao2, conexao.m_idCliente==conexao2.c_id).join(conexao4, conexao4.t_idVendedor==conexao3.v_id).filter(conexao.m_idDev!="", conexao.m_ativo==1, conexao.m_numDoc==conexao4.t_numDoc, conexao.m_parcela==conexao4.t_numParcela, conexao.m_dataBaixa>=dataDe, conexao.m_dataBaixa<=dataAte).order_by(conexao.m_dataBaixa)
                
                linhas = DB.session.query(conexao.m_dataBaixa, conexao.m_docRef, conexao.m_numDoc, conexao.m_valor, conexao.m_parcela , 
                                          conexao2.c_razaosocial.label("cliente"), conexao3.v_nome.label("vendedor"), conexao.m_tipoBaixa, 
                                          conexao4.t_saldo.label("saldo")).join(conexao2, conexao.m_idCliente==conexao2.c_id).join(conexao4, conexao4.t_idVendedor==conexao3.v_id).filter(conexao.m_idDev!="", conexao.m_ativo==1, conexao.m_numDoc==conexao4.t_numDoc, conexao.m_parcela==conexao4.t_numParcela, conexao.m_dataBaixa>=dataDe, conexao.m_dataBaixa<=dataAte).count()
                
                nomeHtml = htmlBaixasDev(baixas, linhas)
                nomeCli = ""
             
            context = {"datas": [dataDe, dataAte], "cliente": nomeCli}
            return render_template(f"impressoes/{nomeHtml}", context=context)
        else:
            return redirect("/")
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro)
        return redirect("/index")

############################################################
# Rota para a impressão do relatório de títulos recebidos
############################################################   
@impressaoBlue.route("/impressao-recebidos", methods=["GET", "POST"])
def impreRecebidos():
    try:
        if session["usuario"]:
            cliVend = ""
            coluna = ""
            descSegmento = ""
            if "cliente" in request.form.keys():
                dataDe = request.form["dataDe"].replace("-", "")
                dataAte = request.form["dataAte"].replace("-", "")
                cliente = list(request.form["cliente"].split())
                cliVend = "Cliente: " + ' '.join(map(str, cliente[2:]))
                conexao = Gf3006
                conexao2 = Gf3003
                conexao3 = Gf3001
                conexao4 = Gf3002
                conexao5 = Gf3004
                conexao6 = Gf3005
                
                baixas = DB.session.query(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, conexao.m_tipoBaixa, conexao.m_deconto, conexao.m_juros,
                                            conexao.m_docRef, conexao4.v_nome.label("vendedor"), conexao.m_valor, 
                                            conexao5.t_saldo.label("saldo"), conexao2.s_abrev.label("segmento"), conexao6.c_valor.label("comissao")).join(conexao2, conexao.m_segmento==conexao2.s_id).join(conexao3, conexao.m_idCliente==conexao3.c_id).join(conexao4, conexao5.t_idVendedor==conexao4.v_id).filter(conexao.m_dataBaixa>=dataDe, conexao.m_dataBaixa<=dataAte, conexao.m_ativo==1, conexao5.t_idCliente==cliente[0], conexao.m_numDoc==conexao5.t_numDoc, conexao.m_parcela==conexao5.t_numParcela, conexao.m_id==conexao6.c_idBaixa).order_by(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela).group_by(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, 
                                            conexao.m_docRef, conexao3.c_razaosocial, conexao.m_valor, 
                                            conexao4.v_nome, conexao5.t_saldo, conexao5.t_comissao, conexao2.s_abrev)
                                            
                linhas = DB.session.query(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, conexao.m_tipoBaixa, conexao.m_deconto, conexao.m_juros,
                                            conexao.m_docRef, conexao4.v_nome.label("vendedor"), conexao.m_valor, 
                                            conexao5.t_saldo.label("saldo"), conexao2.s_abrev.label("segmento"), conexao6.c_valor.label("comissao")).join(conexao2, conexao.m_segmento==conexao2.s_id).join(conexao3, conexao.m_idCliente==conexao3.c_id).join(conexao4, conexao5.t_idVendedor==conexao4.v_id).filter(conexao.m_dataBaixa>=dataDe, conexao.m_dataBaixa<=dataAte, conexao.m_ativo==1, conexao5.t_idCliente==cliente[0], conexao.m_numDoc==conexao5.t_numDoc, conexao.m_parcela==conexao5.t_numParcela, conexao.m_id==conexao6.c_idBaixa).order_by(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela).group_by(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, 
                                            conexao.m_docRef, conexao3.c_razaosocial, conexao.m_valor, 
                                            conexao4.v_nome, conexao5.t_saldo, conexao5.t_comissao, conexao2.s_abrev).count()
                
                nomeHtml = htmlRecebCli(baixas, linhas)
                print(nomeHtml)
                titulo = "Baixas por Cliente"
                coluna = "Vendedor"      
                
            elif "vendedor" in request.form.keys(): 
                dataDe = request.form["dataDe"].replace("-", "")
                dataAte = request.form["dataAte"].replace("-", "")
                vendedor = list(request.form["vendedor"].split())
                cliVend = "Vendedor: " + ' '.join(map(str, vendedor[2:]))
                conexao = Gf3006
                conexao2 = Gf3003
                conexao3 = Gf3001
                conexao4 = Gf3002
                conexao5 = Gf3004
                conexao6 = Gf3005
                
                baixas = DB.session.query(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, conexao.m_tipoBaixa, conexao.m_deconto, conexao.m_juros,
                                            conexao.m_docRef, conexao3.c_razaosocial.label("cliente"), conexao.m_valor, 
                                            conexao5.t_saldo.label("saldo"), conexao2.s_abrev.label("segmento"), conexao6.c_valor.label("comissao")).join(conexao2, conexao.m_segmento==conexao2.s_id).join(conexao3, conexao.m_idCliente==conexao3.c_id).join(conexao4, conexao5.t_idVendedor==conexao4.v_id).filter(conexao.m_dataBaixa>=dataDe, conexao.m_dataBaixa<=dataAte, conexao.m_ativo==1, conexao5.t_idVendedor==vendedor[0], conexao.m_numDoc==conexao5.t_numDoc, conexao.m_parcela==conexao5.t_numParcela, conexao.m_id==conexao6.c_idBaixa).order_by(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela).group_by(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, 
                                            conexao.m_docRef, conexao3.c_razaosocial, conexao.m_valor, 
                                            conexao4.v_nome, conexao5.t_saldo, conexao5.t_comissao, conexao2.s_abrev)
                                            
                linhas = DB.session.query(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, conexao.m_tipoBaixa, conexao.m_deconto, conexao.m_juros,
                                            conexao.m_docRef, conexao3.c_razaosocial.label("cliente"), conexao.m_valor, 
                                            conexao5.t_saldo.label("saldo"), conexao2.s_abrev.label("segmento"), conexao6.c_valor.label("comissao")).join(conexao2, conexao.m_segmento==conexao2.s_id).join(conexao3, conexao.m_idCliente==conexao3.c_id).join(conexao4, conexao5.t_idVendedor==conexao4.v_id).filter(conexao.m_dataBaixa>=dataDe, conexao.m_dataBaixa<=dataAte, conexao.m_ativo==1, conexao5.t_idVendedor==vendedor[0], conexao.m_numDoc==conexao5.t_numDoc, conexao.m_parcela==conexao5.t_numParcela, conexao.m_id==conexao6.c_idBaixa).order_by(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela).group_by(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, 
                                            conexao.m_docRef, conexao3.c_razaosocial, conexao.m_valor, 
                                            conexao4.v_nome, conexao5.t_saldo, conexao5.t_comissao, conexao2.s_abrev).count()
                                            
                nomeHtml = htmlRecebVend(baixas, linhas)
                titulo = "Baixas por Vendedor"
                coluna = "Cliente"
                
            elif "segmento" in request.form.keys():
                dataDe = request.form["dataDe"].replace("-", "")
                dataAte = request.form["dataAte"].replace("-", "")
                segmento = request.form["segmento"]
                
                conexao = Gf3006
                conexao2 = Gf3003
                conexao3 = Gf3001
                conexao4 = Gf3002
                conexao5 = Gf3004
                conexao6 = Gf3005
                if segmento == "0":
                    baixas = DB.session.query(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, conexao.m_tipoBaixa, conexao.m_deconto, conexao.m_juros,
                                            conexao.m_docRef, conexao3.c_razaosocial.label("cliente"), conexao.m_valor, 
                                            conexao4.v_nome.label("vendedor"), conexao5.t_saldo.label("saldo"), conexao6.c_valor.label("comissao"), conexao2.s_abrev.label("segmento"), conexao2.s_desc.label("descSeg")).join(conexao2, conexao.m_segmento==conexao2.s_id).join(conexao3, conexao.m_idCliente==conexao3.c_id).join(conexao4, conexao5.t_idVendedor==conexao4.v_id).filter(conexao.m_dataBaixa>=dataDe, conexao.m_dataBaixa<=dataAte, conexao.m_ativo==1, conexao.m_numDoc==conexao5.t_numDoc, conexao.m_parcela==conexao5.t_numParcela, conexao.m_id==conexao6.c_idBaixa).order_by(conexao2.s_abrev, conexao.m_dataBaixa).group_by(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, 
                                            conexao.m_docRef, conexao3.c_razaosocial, conexao.m_valor, 
                                            conexao4.v_nome, conexao5.t_saldo, conexao5.t_comissao, conexao2.s_abrev)
                                            
                    linhas = DB.session.query(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, 
                                            conexao.m_docRef, conexao3.c_razaosocial, conexao.m_valor, 
                                            conexao4.v_nome, conexao5.t_saldo, conexao5.t_comissao, conexao2.s_abrev, conexao2.s_desc).join(conexao2, conexao.m_segmento==conexao2.s_id).join(conexao3, conexao.m_idCliente==conexao3.c_id).join(conexao4, conexao5.t_idVendedor==conexao4.v_id).filter(conexao.m_dataBaixa>=dataDe, conexao.m_dataBaixa<=dataAte, conexao.m_ativo==1, conexao.m_numDoc==conexao5.t_numDoc, conexao.m_parcela==conexao5.t_numParcela, conexao.m_id==conexao6.c_idBaixa).order_by(conexao2.s_abrev, conexao.m_dataBaixa).group_by(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, 
                                            conexao.m_docRef, conexao3.c_razaosocial, conexao.m_valor, 
                                            conexao4.v_nome, conexao5.t_saldo, conexao5.t_comissao, conexao2.s_abrev).count()
                    seg = True
                    descSegmento = "Todos"
                else:
                    baixas = DB.session.query(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, conexao.m_tipoBaixa, conexao.m_deconto, conexao.m_juros,
                                            conexao.m_docRef, conexao3.c_razaosocial.label("cliente"), conexao.m_valor, 
                                            conexao4.v_nome.label("vendedor"), conexao5.t_saldo.label("saldo"), conexao6.c_valor.label("comissao"), conexao2.s_abrev.label("segmento")).join(conexao2, conexao.m_segmento==conexao2.s_id).join(conexao3, conexao.m_idCliente==conexao3.c_id).join(conexao4, conexao5.t_idVendedor==conexao4.v_id).filter(conexao.m_dataBaixa>=dataDe, conexao.m_dataBaixa<=dataAte, conexao.m_ativo==1, conexao.m_segmento==segmento, conexao.m_numDoc==conexao5.t_numDoc, conexao.m_parcela==conexao5.t_numParcela, conexao.m_id==conexao6.c_idBaixa).order_by(conexao2.s_abrev, conexao.m_dataBaixa).group_by(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, 
                                            conexao.m_docRef, conexao3.c_razaosocial, conexao.m_valor, 
                                            conexao4.v_nome, conexao5.t_saldo, conexao5.t_comissao, conexao2.s_abrev)
                                            
                    linhas = DB.session.query(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, 
                                            conexao.m_docRef, conexao3.c_razaosocial, conexao.m_valor, 
                                            conexao4.v_nome, conexao5.t_saldo, conexao5.t_comissao, conexao2.s_abrev).join(conexao2, conexao.m_segmento==conexao2.s_id).join(conexao3, conexao.m_idCliente==conexao3.c_id).join(conexao4, conexao5.t_idVendedor==conexao4.v_id).filter(conexao.m_dataBaixa>=dataDe, conexao.m_dataBaixa<=dataAte, conexao.m_ativo==1, conexao.m_segmento==segmento, conexao.m_numDoc==conexao5.t_numDoc, conexao.m_parcela==conexao5.t_numParcela, conexao.m_id==conexao6.c_idBaixa).order_by(conexao2.s_abrev, conexao.m_dataBaixa).group_by(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, 
                                            conexao.m_docRef, conexao3.c_razaosocial, conexao.m_valor, 
                                            conexao4.v_nome, conexao5.t_saldo, conexao5.t_comissao, conexao2.s_abrev).count()
                    seg = False
                    descSegmento = conexao2.query.filter(conexao2.s_id==segmento).first()
                    descSegmento = descSegmento.s_desc
               
                nomeHtml = htmlRecebSegmento(baixas, linhas, seg)  
                titulo = "Baixas por Segmento"      
            
            elif "dataDeMes" in request.form.keys():
                dataDe = request.form["dataDeMes"].replace("-", "")
                dataAte = request.form["dataAteMes"].replace("-", "")
                conexao = Gf3006
                conexao2 = Gf3003
                conexao3 = Gf3001
                conexao4 = Gf3002
                conexao5 = Gf3004
                conexao6 = Gf3005
                baixas = DB.session.query(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, conexao.m_tipoBaixa, conexao.m_deconto, conexao.m_juros, conexao.m_docRef, conexao3.c_razaosocial.label("cliente"), conexao.m_valor, conexao4.v_nome.label("vendedor"), conexao5.t_saldo.label("saldo"), conexao2.s_abrev.label("segmento"), conexao6.c_valor.label("comissao"), conexao5.t_dataLanc.label("lancamento")).join(conexao2, conexao.m_segmento==conexao2.s_id).join(conexao3, conexao.m_idCliente==conexao3.c_id).join(conexao4, conexao5.t_idVendedor==conexao4.v_id).filter(conexao.m_dataBaixa>=dataDe, conexao.m_dataBaixa<=dataAte, conexao.m_ativo==1, conexao.m_numDoc==conexao5.t_numDoc, 
                conexao.m_parcela==conexao5.t_numParcela, conexao.m_id==conexao6.c_idBaixa).order_by(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela).group_by(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, conexao.m_docRef, conexao3.c_razaosocial, conexao.m_valor, conexao4.v_nome, conexao5.t_saldo, conexao5.t_comissao, conexao2.s_abrev)
                                            
                linhas = DB.session.query(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, conexao.m_tipoBaixa, conexao.m_deconto, conexao.m_juros, conexao.m_docRef, conexao3.c_razaosocial.label("cliente"), conexao.m_valor, conexao4.v_nome.label("vendedor"), conexao5.t_saldo.label("saldo"), conexao2.s_abrev.label("segmento"), conexao6.c_valor.label("comissao"), conexao5.t_dataLanc.label("lancamento")).join(conexao2, conexao.m_segmento==conexao2.s_id).join(conexao3, conexao.m_idCliente==conexao3.c_id).join(conexao4, conexao5.t_idVendedor==conexao4.v_id).filter(conexao.m_dataBaixa>=dataDe, conexao.m_dataBaixa<=dataAte, conexao.m_ativo==1, conexao.m_numDoc==conexao5.t_numDoc, 
                conexao.m_parcela==conexao5.t_numParcela, conexao.m_id==conexao6.c_idBaixa).order_by(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela).group_by(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, conexao.m_docRef, conexao3.c_razaosocial, conexao.m_valor, conexao4.v_nome, conexao5.t_saldo, conexao5.t_comissao, conexao2.s_abrev).count()
                                    
                nomeHtml = htmlRecebPeriodoMes(baixas, linhas)                          
                titulo = "Baixas por Periodo"
                
            else:
                dataDe = request.form["dataDe"].replace("-", "")
                dataAte = request.form["dataAte"].replace("-", "")
                conexao = Gf3006
                conexao2 = Gf3003
                conexao3 = Gf3001
                conexao4 = Gf3002
                conexao5 = Gf3004
                conexao6 = Gf3005
                baixas = DB.session.query(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, conexao.m_tipoBaixa, conexao.m_deconto, conexao.m_juros, conexao.m_docRef, conexao3.c_razaosocial.label("cliente"), conexao.m_valor, conexao4.v_nome.label("vendedor"), conexao5.t_saldo.label("saldo"), conexao2.s_abrev.label("segmento"), conexao6.c_valor.label("comissao")).join(conexao2, conexao.m_segmento==conexao2.s_id).join(conexao3, conexao.m_idCliente==conexao3.c_id).join(conexao4, conexao5.t_idVendedor==conexao4.v_id).filter(conexao.m_dataBaixa>=dataDe, conexao.m_dataBaixa<=dataAte, conexao.m_ativo==1, conexao.m_numDoc==conexao5.t_numDoc, 
                conexao.m_parcela==conexao5.t_numParcela, conexao.m_id==conexao6.c_idBaixa).order_by(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela).group_by(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, conexao.m_docRef, conexao3.c_razaosocial, conexao.m_valor, conexao4.v_nome, conexao5.t_saldo, conexao5.t_comissao, conexao2.s_abrev)
                                            
                linhas = DB.session.query(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, conexao.m_tipoBaixa, 
                                            conexao.m_docRef, conexao3.c_razaosocial.label("cliente"), conexao.m_valor, 
                                            conexao4.v_nome.label("vendedor"), conexao5.t_saldo.label("saldo"), conexao2.s_abrev.label("segmento"), conexao6.c_valor.label("comissao")).join(conexao2, conexao.m_segmento==conexao2.s_id).join(conexao3, conexao.m_idCliente==conexao3.c_id).join(conexao4, conexao5.t_idVendedor==conexao4.v_id).filter(conexao.m_dataBaixa>=dataDe, conexao.m_dataBaixa<=dataAte, conexao.m_ativo==1, conexao.m_numDoc==conexao5.t_numDoc, conexao.m_parcela==conexao5.t_numParcela, conexao.m_id==conexao6.c_idBaixa).order_by(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela).group_by(conexao.m_dataBaixa, conexao.m_numDoc, conexao.m_parcela, 
                                            conexao.m_docRef, conexao3.c_razaosocial, conexao.m_valor, 
                                            conexao4.v_nome, conexao5.t_saldo, conexao5.t_comissao, conexao2.s_abrev).count()
                                    
                nomeHtml = htmlRecebPeriodo(baixas, linhas)                          
                titulo = "Baixas por Periodo"
            
            context = {"titulo": titulo, "datas": [dataDe, dataAte], "cliVend": cliVend, "coluna": coluna, "descSegmento": descSegmento}
            return render_template(f"impressoes/{nomeHtml}", context=context)
        else:
            return redirect("/")
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro)
        return redirect("/index")
    
############################################################
# Rota para a impressão do relatório de títulos a receber
############################################################
@impressaoBlue.route("/impressao-receber", methods=["GET", "POST"])
def impreReceber():
    try:
        if session["usuario"]:
            cliVend = ""
            coluna = ""
            descSegmento = ""
            if "cliente" in request.form.keys():
                dataDe = request.form["dataDe"].replace("-", "")
                dataAte = request.form["dataAte"].replace("-", "")
                cliente = list(request.form["cliente"].split())
                cliVend = "Cliente: " + ' '.join(map(str, cliente[2:]))
                conexao = Gf3004
                conexao2 = Gf3001
                conexao3 = Gf3002
                conexao4 = Gf3003
                
                baixas = DB.session.query(conexao.t_numDoc, conexao.t_numParcela, conexao.t_docRef, 
                                          conexao.t_dataVenc, conexao2.c_razaosocial.label("cliente"), 
                                          conexao3.v_nome.label("vendedor"), conexao.t_saldo, conexao4.s_abrev.label("segmento")).join(conexao2, conexao.t_idCliente==conexao2.c_id).join(conexao3, conexao.t_idVendedor==conexao3.v_id).join(conexao4, conexao.t_segmento==conexao4.s_id).filter(conexao.t_ativo==1, conexao.t_status==1, conexao.t_dataLanc>=dataDe, conexao.t_dataLanc<=dataAte, conexao.t_idCliente==cliente[0]).order_by(conexao.t_dataVenc)
                
                linhas = DB.session.query(conexao.t_numDoc, conexao.t_numParcela, conexao.t_docRef, 
                                          conexao.t_dataVenc, conexao2.c_razaosocial.label("cliente"), 
                                          conexao3.v_nome.label("vendedor"), conexao.t_saldo, conexao4.s_abrev.label("segmento")).join(conexao2, conexao.t_idCliente==conexao2.c_id).join(conexao3, conexao.t_idVendedor==conexao3.v_id).join(conexao4, conexao.t_segmento==conexao4.s_id).filter(conexao.t_ativo==1, conexao.t_status==1, conexao.t_dataLanc>=dataDe, conexao.t_dataLanc<=dataAte, conexao.t_idCliente==cliente[0]).order_by(conexao.t_dataVenc).count()
                
                nomeHtml = htmlReceberbCli(baixas, linhas)
                titulo = "Títulos a Receber por Cliente"
                coluna = "Vendedor"      
                
            elif "vendedor" in request.form.keys(): 
                dataDe = request.form["dataDe"].replace("-", "")
                dataAte = request.form["dataAte"].replace("-", "")
                vendedor = list(request.form["vendedor"].split())
                cliVend = "Vendedor: " + ' '.join(map(str, vendedor[2:]))
                conexao = Gf3004
                conexao2 = Gf3001
                conexao3 = Gf3002
                conexao4 = Gf3003
                
                baixas = DB.session.query(conexao.t_numDoc, conexao.t_numParcela, conexao.t_docRef, 
                                          conexao.t_dataVenc, conexao2.c_razaosocial.label("cliente"), 
                                          conexao3.v_nome.label("vendedor"), conexao.t_saldo, conexao4.s_abrev.label("segmento")).join(conexao2, conexao.t_idCliente==conexao2.c_id).join(conexao3, conexao.t_idVendedor==conexao3.v_id).join(conexao4, conexao.t_segmento==conexao4.s_id).filter(conexao.t_ativo==1, conexao.t_status==1, conexao.t_dataLanc>=dataDe, conexao.t_dataLanc<=dataAte, conexao.t_idVendedor==vendedor[0]).order_by(conexao.t_dataVenc)
                
                linhas =  DB.session.query(conexao.t_numDoc, conexao.t_numParcela, conexao.t_docRef, 
                                          conexao.t_dataVenc, conexao2.c_razaosocial.label("cliente"), 
                                          conexao3.v_nome.label("vendedor"), conexao.t_saldo, conexao4.s_abrev.label("segmento")).join(conexao2, conexao.t_idCliente==conexao2.c_id).join(conexao3, conexao.t_idVendedor==conexao3.v_id).join(conexao4, conexao.t_segmento==conexao4.s_id).filter(conexao.t_ativo==1, conexao.t_status==1, conexao.t_dataLanc>=dataDe, conexao.t_dataLanc<=dataAte, conexao.t_idVendedor==vendedor[0]).order_by(conexao.t_dataVenc).count()
                                            
                                            
                nomeHtml = htmlReceberbVend(baixas, linhas)
                titulo = "Títulos a Receber por Vendedor"
                coluna = "Cliente"
                
            elif "segmento" in request.form.keys():
                dataDe = request.form["dataDe"].replace("-", "")
                dataAte = request.form["dataAte"].replace("-", "")
                segmento = request.form["segmento"]
                
                conexao = Gf3004
                conexao2 = Gf3001
                conexao3 = Gf3002
                conexao4 = Gf3003
                if segmento == "0":
                    baixas = DB.session.query(conexao.t_numDoc, conexao.t_numParcela, conexao.t_docRef, 
                                          conexao.t_dataVenc, conexao2.c_razaosocial.label("cliente"), 
                                          conexao3.v_nome.label("vendedor"), conexao.t_saldo, conexao4.s_abrev.label("segmento"), conexao4.s_desc.label("descSeg")).join(conexao2, conexao.t_idCliente==conexao2.c_id).join(conexao3, conexao.t_idVendedor==conexao3.v_id).join(conexao4, conexao.t_segmento==conexao4.s_id).filter(conexao.t_ativo==1, conexao.t_status==1, conexao.t_dataLanc>=dataDe, conexao.t_dataLanc<=dataAte).order_by(conexao4.s_abrev, conexao.t_dataVenc)
                
                    linhas = DB.session.query(conexao.t_numDoc, conexao.t_numParcela, 
                                            conexao.t_dataVenc, conexao2.c_razaosocial.label("cliente"), 
                                            conexao3.v_nome.label("vendedor"), conexao.t_saldo, conexao4.s_abrev.label("segmento"), conexao4.s_desc.label("descSeg")).join(conexao2, conexao.t_idCliente==conexao2.c_id).join(conexao3, conexao.t_idVendedor==conexao3.v_id).join(conexao4, conexao.t_segmento==conexao4.s_id).filter(conexao.t_ativo==1, conexao.t_status==1, conexao.t_dataLanc>=dataDe, conexao.t_dataLanc<=dataAte).order_by(conexao4.s_abrev, conexao.t_dataVenc).count()
                    seg = True
                    descSegmento = "Todos"
                else:
                    baixas = DB.session.query(conexao.t_numDoc, conexao.t_numParcela, conexao.t_docRef, 
                                          conexao.t_dataVenc, conexao2.c_razaosocial.label("cliente"), 
                                          conexao3.v_nome.label("vendedor"), conexao.t_saldo, conexao4.s_abrev.label("segmento"), conexao4.s_desc.label("descSegmento")).join(conexao2, conexao.t_idCliente==conexao2.c_id).join(conexao3, conexao.t_idVendedor==conexao3.v_id).join(conexao4, conexao.t_segmento==conexao4.s_id).filter(conexao.t_ativo==1, conexao.t_status==1, conexao.t_dataLanc>=dataDe, conexao.t_dataLanc<=dataAte, conexao.t_segmento==segmento).order_by(conexao4.s_abrev, conexao.t_dataVenc)
                
                    linhas = DB.session.query(conexao.t_numDoc, conexao.t_numParcela, 
                                            conexao.t_dataVenc, conexao2.c_razaosocial.label("cliente"), 
                                            conexao3.v_nome.label("vendedor"), conexao.t_saldo, conexao4.s_desc).join(conexao2, conexao.t_idCliente==conexao2.c_id).join(conexao3, conexao.t_idVendedor==conexao3.v_id).join(conexao4, conexao.t_segmento==conexao4.s_id).filter(conexao.t_ativo==1, conexao.t_status==1, conexao.t_dataLanc>=dataDe, conexao.t_dataLanc<=dataAte, conexao.t_segmento==segmento).order_by(conexao4.s_abrev, conexao.t_dataVenc).count()
                    seg = False
                    descSegmento = conexao4.query.filter(conexao4.s_id==segmento).first()
                    descSegmento = descSegmento.s_desc
               
                nomeHtml = htmlReceberSegmento(baixas, linhas, seg)  
                titulo = "Títulos a Receber por Segmento" 
            
            elif "docDe" in request.form.keys():
                docDe = request.form["docDe"]
                docAte = request.form["docAte"]
                listaDoc = []
                conexao = Gf3004
                
                docs = DB.session.query(conexao.t_numDoc).distinct(conexao.t_numDoc).filter(conexao.t_numDoc>=docDe, conexao.t_numDoc<=docAte, conexao.t_ativo==1, conexao.t_status==1).order_by(conexao.t_numDoc)
                
                for doc in docs:
                    listaDoc.append(doc.t_numDoc)
                
                nomeHtml = htmlPlanilha(listaDoc)
                titulo = "Títulos a Receber"
                context = {"titulo": titulo}
                return render_template(f"impressoes/{nomeHtml}", context=context)
                
            else:
                dataDe = request.form["dataDe"].replace("-", "")
                dataAte = request.form["dataAte"].replace("-", "")
                conexao = Gf3004
                conexao2 = Gf3001
                conexao3 = Gf3002
                conexao4 = Gf3003
                
                baixas = DB.session.query(conexao.t_numDoc, conexao.t_numParcela, conexao.t_docRef, 
                                          conexao.t_dataVenc, conexao2.c_razaosocial.label("cliente"), 
                                          conexao3.v_nome.label("vendedor"), conexao.t_saldo, conexao4.s_abrev.label("segmento")).join(conexao2, conexao.t_idCliente==conexao2.c_id).join(conexao3, conexao.t_idVendedor==conexao3.v_id).join(conexao4, conexao.t_segmento==conexao4.s_id).filter(conexao.t_ativo==1, conexao.t_status==1, conexao.t_dataLanc>=dataDe, conexao.t_dataLanc<=dataAte).order_by(conexao.t_dataVenc)
                
                linhas = DB.session.query(conexao.t_numDoc, conexao.t_numParcela, 
                                          conexao.t_dataVenc, conexao2.c_razaosocial.label("cliente"), 
                                          conexao3.v_nome.label("vendedor"), conexao.t_saldo, conexao4.s_desc).join(conexao2, conexao.t_idCliente==conexao2.c_id).join(conexao3, conexao.t_idVendedor==conexao3.v_id).join(conexao4, conexao.t_segmento==conexao4.s_id).filter(conexao.t_ativo==1, conexao.t_status==1, conexao.t_dataLanc>=dataDe, conexao.t_dataLanc<=dataAte).order_by(conexao.t_dataVenc).count()
                                           
                nomeHtml = htmlReceberPeriodo(baixas, linhas)
                titulo = "Títulos a Receber"
            
            context = {"titulo": titulo, "datas": [dataDe, dataAte], "cliVend": cliVend, "coluna": coluna, "descSegmento": descSegmento}
            return render_template(f"impressoes/{nomeHtml}", context=context)

        else:
            return redirect("/")
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro)
        return redirect("/index")
           
############################################################
# Rota para a impressão do relatório de comissões
############################################################
@impressaoBlue.route("/impressao-consistencia", methods=["GET", "POST"])
def impreConsisitencia():
    try:
        if session["usuario"]:
            
            if "dataDeCli" in request.form.keys():
                dataDe = request.form["dataDeCli"].replace("-", "")
                dataAte = request.form["dataAteCli"].replace("-", "")
                conexao = Gf3004
                
                titulos = DB.session.query(conexao.t_idCliente).distinct(conexao.t_idCliente).filter(conexao.t_dataLanc>=dataDe, conexao.t_dataLanc<=dataAte, conexao.t_ativo==1).order_by(conexao.t_dataLanc)
                
                titulo = "Relatório de Consistência"
                nomeHtml = htmlConsisCli(titulos, dataDe, dataAte)
                context = {"titulo": titulo, "datas": [dataDe, dataAte]}
                return render_template(f"impressoes/{nomeHtml}", context=context)
                
            else:
                dataDe = request.form["dataDe"].replace("-", "")
                dataAte = request.form["dataAte"].replace("-", "")
                conexao = Gf3004
                conexao2 = Gf3001
                conexao3 = Gf3002
                conexao4 = Gf3003
                
                titulos = DB.session.query(conexao.t_numDoc, conexao.t_numParcela, conexao.t_dataLanc, conexao.t_dataVenc, conexao2.c_razaosocial.label("cliente"), conexao3.v_nome.label("vendedor"), 
                conexao4.s_abrev.label("segmento"), conexao4.s_desc.label("decSeg"), conexao.t_docRef, conexao.t_saldo, conexao.t_valor, conexao.t_status) \
                .join(conexao2, conexao2.c_id==conexao.t_idCliente) \
                .join(conexao3, conexao3.v_id==conexao.t_idVendedor) \
                .join(conexao4, conexao4.s_id==conexao.t_segmento) \
                .filter(conexao.t_dataLanc>=dataDe, conexao.t_dataLanc<=dataAte, conexao.t_ativo==1) \
                .order_by(conexao4.s_abrev, conexao.t_dataLanc)
                
                linhas = DB.session.query(conexao.t_numDoc, conexao.t_numParcela, conexao.t_dataLanc, conexao.t_dataVenc, conexao2.c_razaosocial.label("cliente"), conexao3.v_nome.label("vendedor"), 
                conexao4.s_abrev.label("segmento"), conexao4.s_desc.label("decSeg"), conexao.t_docRef, conexao.t_saldo, conexao.t_valor, conexao.t_status) \
                .join(conexao2, conexao2.c_id==conexao.t_idCliente) \
                .join(conexao3, conexao3.v_id==conexao.t_idVendedor) \
                .join(conexao4, conexao4.s_id==conexao.t_segmento) \
                .filter(conexao.t_dataLanc>=dataDe, conexao.t_dataLanc<=dataAte, conexao.t_ativo==1) \
                .order_by(conexao4.s_abrev, conexao.t_dataLanc).count()
                
                titulo = "Relatório de Consistência"
                nomeHtml = htmlConsis(titulos, linhas)
                context = {"titulo": titulo, "datas": [dataDe, dataAte]}
                return render_template(f"impressoes/{nomeHtml}", context=context)
            
        else:
            return redirect("/")
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro)
        return redirect("/index")
    
############################################################
# Rota para a impressão do relatório de comissões
############################################################
@impressaoBlue.route("/impressao-observacao", methods=["GET", "POST"])
def impreObservacao():
    try:
        if session["usuario"]:
            dataDe = request.form["dataDe"].replace("-", "")
            dataAte = request.form["dataAte"].replace("-", "")
            conexao = Gf3006
            
            idObserv = DB.session.query(conexao.m_id) \
            .filter(conexao.m_dataBaixa>=dataDe, conexao.m_dataBaixa<=dataAte, conexao.m_ativo==1, conexao.m_observ!=None) \
            .order_by(conexao.m_id)
            
            listaId = []
            
            for id in idObserv:
                listaId.append(id.m_id)
            
            nomeHtml = htmlObservacao(listaId)
            return render_template(f"impressoes/{nomeHtml}")
            
        else:
            return redirect("/")
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro)
        return redirect("/index")