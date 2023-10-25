from ..httpResponse.HttpResponse import HttpResponse
from ..models.Models import Gf3003
from .ControllerFiltros import *
from flask_login import login_required
from ..extensions.Log import Log
from flask import request, abort
import traceback
import sys

class ControllerRelatorio(HttpResponse, Log):
    """
    Classe Controller para as funções relacionadas aos Relatórios
    @author - Fabio
    @tables - Gf3003
    @version - 1.0
    @since - 23/10/2023
    """

    @login_required
    def renderRelatComissao(self) -> HttpResponse:
        try:
            context = {"active": "relatComi", "titulo": "Parâmetros para o relatório de comissão"}
            return self.responseRender(arquivo="relatorios/relatComissao.html", context=context)

        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)

    
    @login_required
    def renderRelatDevolucao(self) -> HttpResponse:
        try:
            context = {"active": "relatDev", "titulo": "Parâmetros para o relatório de devoluções"}
            return self.responseRender(arquivo="relatorios/relatDevolucao.html", context=context)

        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def renderRelatRecebidos(self) -> HttpResponse:
        try:
            segmentos = Gf3003.query.filter()
            context = {"segmentos": segmentos, "active": "relatRecebidos", "titulo": "Parâmetros para o relatório de títulos recebidos"}
            return self.responseRender(arquivo="relatorios/relatRecebidos.html", context=context)

        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def renderRelatReceber(self) -> HttpResponse:
        try:
            segmentos = Gf3003.query.filter()
            context = {"segmentos": segmentos, "active": "relatReceber", "titulo": "Parâmetros para o relatório de títulos a receber"}
            return self.responseRender(arquivo="relatorios/relatReceber.html", context=context)

        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def renderRelatConsistencia(self) -> HttpResponse:
        try:
            context = {"active": "relatConsis", "titulo": "Parâmetros para o relatório de consistência"}
            return self.responseRender(arquivo="relatorios/relatConsistencia.html", context=context)

        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)

    
    @login_required
    def renderRelatObservacao(self) -> HttpResponse:
        try:
            context = {"active": "relatObs", "titulo": "Parâmetros para o relatório de observações"}
            return self.responseRender(arquivo="relatorios/relatObservacao.html", context=context)

        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)
