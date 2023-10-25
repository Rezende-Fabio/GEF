from ..httpResponse.HttpResponse import HttpResponse
from ..models.Models import Gf3006, Gf3001
from .ControllerFiltros import *
from ..configurations.DataBase import DB
from flask_login import login_required
from ..extensions.Log import Log
from flask import request, abort
import traceback
import sys

class ControllerObservacoes(HttpResponse, Log):
    """
    Classe Controller para as funções relacionadas as Observações
    @author - Fabio
    @tables - Gf3001
    @version - 1.0
    @since - 23/10/2023
    """

    @login_required
    def renderListaObservacoes(self) -> HttpResponse:
        try:
            context = {"active": "observacao", "titulo": "Observações"}
            return self.responseRender(arquivo="observacoes/listaObservacoes.html", context=context)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def consultarObservacoes(self) -> HttpResponse:
        try:            
            baixas = DB.session.query(Gf3006.m_numDoc, Gf3006.m_observ, Gf3006.m_parcela, Gf3006.m_dataBaixa, Gf3006.m_valor, Gf3006.m_docRef, Gf3001.c_razaosocial.label("cliente"))\
            .join(Gf3001, Gf3006.m_idCliente==Gf3001.c_id).filter(Gf3006.m_observ!="", Gf3006.m_ativo==1)
            listaObs = []
            for x in baixas:  
                listaObs.append({"ref": x.m_docRef, "doc": x.m_numDoc, "par": x.m_parcela, "cli": filtroNome(x.cliente), "lanc": filtroData(x.m_dataBaixa), "valor": filtroValor(x.m_valor)})  
            return self.responseJson(body=listaObs, status=200)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def consultarObservacao(self, doc: int, parc: int) -> HttpResponse:
        try:
            baixa = DB.session.query(Gf3006.m_numDoc, Gf3006.m_docRef, Gf3006.m_parcela, Gf3006.m_dataBaixa, Gf3006.m_valor, Gf3006.m_juros, Gf3006.m_deconto, Gf3006.m_tipoBaixa, Gf3006.m_observ, Gf3001.c_razaosocial.label("cliente"), Gf3006.m_idCliente)\
            .join(Gf3001, Gf3006.m_idCliente==Gf3001.c_id).filter(Gf3006.m_numDoc==doc, Gf3006.m_parcela==parc, Gf3006.m_observ!=None).first()
            context = {"baixa": baixa}  #Dicionário contendo as variáveis para utilizar no template
            return self.responseRender("observacoes/corpoModalVisuObs.html", context=context)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)
