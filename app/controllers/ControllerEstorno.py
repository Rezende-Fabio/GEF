from ..httpResponse.HttpResponse import HttpResponse
from ..controllers.ControllerFiltros import *
from ..models.Models import Gf3004, Gf3006, Gf3007, Gf3005
from flask import session, abort, request
from ..configurations.DataBase import DB
from flask_login import login_required
from ..extensions.Log import Log
from datetime import datetime
import traceback
import sys

class ControllerEstorno(HttpResponse, Log):
    """
    Classe Controller para as funções relacionadas ao Estorno
    @author - Fabio
    @tables - Gf3004
    @version - 1.0
    @since - 25/10/2023
    """

    @login_required
    def renderListaEstorno(self) -> HttpResponse:
        try:
            context = {"active": "estorno", "titulo": "Lista de Estornos"}
            return self.responseRender(arquivo="estorno/listaEstorno.html", context=context)

        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def consultarBaixasParaEstornos(self) -> HttpResponse:
        try:
            dataAtual = datetime.now().strftime("%Y")
            #Query que trás todos os títulos que estão baixados
            estornos = Gf3004.query.filter(Gf3004.t_ativo==1, Gf3004.t_saldo!=Gf3004.t_valor, Gf3004.t_dataLanc>=dataAtual).order_by(Gf3004.t_dataVenc)
            
            listaEstornos = []
            for estorno in estornos:
                dictEstorno = {
                    "ref": estorno.t_segmento.s_abrev + estorno.t_docRef, 
                    "doc": estorno.t_numDoc, 
                    "par": estorno.t_numParcela, 
                    "cli": filtroNome(estorno.t_cliente.c_razaosocial), 
                    "vend": filtroNome(estorno.t_vendedor.v_nome), 
                    "lanc": filtroData(estorno.t_dataLanc), 
                    "venc":filtroData(estorno.t_dataVenc)
                }
                listaEstornos.append(dictEstorno)
            
            return self.responseJson(body=listaEstornos, status=200)

        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def renderConsultarBaixasParaEstorno(self, doc: int, parcela: int) -> HttpResponse:
        try:
            baixas = Gf3006.query.filter(Gf3006.m_numDoc==doc, Gf3006.m_parcela==parcela, Gf3006.m_ativo==True)
            context = {"baixas": baixas}
            return self.responseRender(arquivo="estorno/corpoModalEstorno.html", context=context)

        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def estornarBaixa(self) -> HttpResponse:
        try:
            listaIds = request.get_json()
            ids = []
            for id in listaIds["list"]:
                ids.append(id)
                
                baixa = Gf3006.query.filter(Gf3006.m_id==id).first()
                baixa.m_ativo = False
                
                if baixa.m_idDev:
                    devolucao = Gf3007.query.filter(Gf3007.d_id==baixa.m_idDev, Gf3007.d_ativo!=False).first()
                    devolucao.estornaCredito(baixa.m_valor)
                else:
                    comissao = Gf3005.query.filter(Gf3005.c_idBaixa==id, Gf3005.c_ativo!=False).first()
                    comissao.c_ativo = False
                
                titulo = Gf3004.query.filter(Gf3004.t_numDoc==baixa.m_numDoc, Gf3004.t_numParcela==baixa.m_parcela).first()
                titulo.estornaSaldo(baixa.m_valor)
            
                DB.session.commit()
                self.geraLogDiario("Estorno de Baixa", session["usuario"]["usuario"], session["filial"], f"Documento: {baixa.m_numDoc} Parcela: {baixa.m_parcela}")
            return self.responseJson(body=ids, status=200)

        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)