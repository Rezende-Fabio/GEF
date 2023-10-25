from ..models.Models import Gf3004, Gf3005, Gf3006, Gf3007
from ..httpResponse.HttpResponse import HttpResponse
from ..decorators.FormBaixa import validaFormBaixa
from ..controllers.ControllerFiltros import *
from flask import request, abort, session
from ..configurations.DataBase import DB
from flask_login import login_required
from ..extensions.Log import Log
from datetime import datetime
from sqlalchemy import func
import traceback
import sys

class ControllerBaixa(HttpResponse, Log):
    """
    Classe Controller para as funções relacionadas as baixas
    @author - Fabio
    @tables - Gf3004, Gf3001, Gf3002, Gf3003, Gf3006
    @version - 1.0
    @since - 24/10/2023
    """
    
    @login_required
    def renderListaBaixas(self) -> HttpResponse:
        try:
            context = {"active": "baixa", "titulo": "Lista de Baixas"}
            return self.responseRender(arquivo="baixa/listaBaixas.html", context=context)
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def consultarBaixas(self) -> HttpResponse:
        try:
            dataAtual = datetime.today().strftime("%Y%m%d")
            #Query que trás todos os títulos que estão em berto 
            baixas = Gf3004.query.filter(Gf3004.t_ativo==True, Gf3004.t_status==True).order_by(Gf3004.t_dataVenc)
            listaBaixas = []
            for baixa in baixas:
                if baixa.t_dataVenc < dataAtual:
                    datavenc = f"<span style='color:red; font-weight: bold;'>{filtroData(baixa.t_dataVenc)}</span>"
                else:
                    datavenc = f"<span>{filtroData(baixa.t_dataVenc)}</span>"

                dicBaixa = {
                    "ref": baixa.t_segmento.s_abrev + baixa.t_docRef, 
                    "doc": baixa.t_numDoc, 
                    "par": baixa.t_numParcela, 
                    "cli": filtroNome(baixa.t_cliente.c_razaosocial), 
                    "vend": filtroNome(baixa.t_vendedor.v_nome), 
                    "lanc": filtroData(baixa.t_dataLanc), 
                    "venc": datavenc, 
                    "saldo": filtroValor(baixa.t_saldo) 
                }

                listaBaixas.append(dicBaixa)

            return self.responseJson(body=listaBaixas, status=200)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)
    
    @login_required
    def renderCadastarBaixa(self, doc: int, parcela: int) -> HttpResponse:
        try:
            #Query que trás o título de acordo com o número do documento e parcela passado
            titulo = Gf3004.query.filter(Gf3004.t_numDoc==doc, Gf3004.t_numParcela==parcela).first()
            #Query que trás o número de parcelas do título
            parcelas = DB.session.query(Gf3004.t_dataVenc, Gf3004.t_valor, Gf3004.t_numParcela).filter(Gf3004.t_numDoc == doc).order_by(Gf3004.t_numParcela)
            #Query que trás o crédito do cliente caso ele tenha
            credito = DB.session.query(Gf3007.d_id).filter(Gf3007.d_idCliente==titulo.t_idCliente, Gf3007.d_status==1, Gf3007.d_ativo==1).join(Gf3004, Gf3004.t_idCliente == Gf3007.d_idCliente).count()
            context = {"tituloDoc": titulo, "parcelas": parcelas, "credito": credito, "active": "baixa", "titulo": "Baixa do Título"} #Dicionário contendo as variáveis para utilizar no template
            
            return self.responseRender(arquivo="baixa/cadBaixa.html", context=context)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    @validaFormBaixa
    def inserirBaixa(self) -> HttpResponse:
        try:
            form = request.form
            idCliente = list(form["cliente"].split())
            if form["valorCredito"] != "":
                idDev = int(form["idDevolucao"])
                
                devolucao = Gf3007.query.filter(Gf3007.d_id==idDev).first()
                
                if float(form["valorSaldo"]) != float(form["valorParcela"]):
                    tipoBaixa = "DP"
                elif devolucao.d_saldo >= float(form["valorParcela"]):
                    tipoBaixa = "DT"
                elif devolucao.d_saldo < float(form["valorParcela"]):
                    tipoBaixa = "DP"
                
                valorBaixa = devolucao.calculaCredito(float(form["valorSaldo"]))
                    
            else:
                valorBaixa = float(form["valorBaixa"])
                
                if float(form["valorBaixa"]) == float(form["valorParcela"]):
                    tipoBaixa = "BT"
                else:
                    tipoBaixa = "BP"
                    
                idDev = None

            if len(form["obs"]) == 0:
                observ = None
            else:
                observ = form["obs"]
                    
            baixa = Gf3006(
                m_numDoc = int(form["numDoc"]),
                m_parcela = int(form["parcela"]),
                m_dataBaixa = form["dataBaixa"].replace("-", ""),
                m_docRef = form["docRef"],
                m_idCliente = idCliente[0],
                m_valor = valorBaixa,
                m_tipoBaixa = tipoBaixa,
                m_filial = int(form["filial"]),
                m_juros = float(form["juros"]),
                m_deconto = float(form["desconto"]),
                m_observ = observ,
                m_usuario = session["usuario"]["usuario"],
                m_idDev = idDev,
                m_idSegmento = int(form["segmento"]),
                m_ativo = True
            )

            #Query que trás o título de acordo com o número dodocumento e a parcela
            titulo = Gf3004.query.filter(Gf3004.t_numDoc==int(form["numDoc"]), Gf3004.t_numParcela==int(form["parcela"])).first()
            titulo.calculaSaldo(valorBaixa) #Calcula o novo saldo do título

            DB.session.add(baixa)
            DB.session.commit()

            if "D" not in tipoBaixa: #Calcula a comisssão caso não seja baixa por devolução
                self.inserirComissao(form)

            self.geraLogDiario("Baixa do Título", session["usuario"]["usuario"], session["filial"], f"Documento: {request.form['numDoc']} Parcela: {request.form['parcela']}") #Gera log informando que foi feita baixa no título 
            return self.responseJsonMessage(status=204, mensagem="Baixa efetuada com sucesso!", categoria="success")
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    def inserirComissao(self, form: dict) -> None:
        #Query que trás o id da última baixa efetuada
        baixa = Gf3006.query.filter(Gf3006.m_numDoc==int(form["numDoc"]), Gf3006.m_parcela==int(form["parcela"])).first()
        
        idVendedor = list(form["vendedor"].split())
        comissao = Gf3005(
            c_idVendedor = idVendedor[0],
            c_baseCalc = baixa.calculaBase(),
            c_idBaixa = baixa.m_id,
            c_valor = baixa.calculaComissao(float(form["comissao"])),
            c_dataBaixa = form["dataBaixa"].replace("-", ""),
            c_docRef = form["docRef"],
            c_numDoc = form["numDoc"],
            c_perc = float(form["comissao"]),
            c_ativo = True
        )
        
        DB.session.add(comissao)
        DB.session.commit()