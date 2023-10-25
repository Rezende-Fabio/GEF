from ..httpResponse.HttpResponse import HttpResponse
from dateutil.relativedelta import relativedelta
from .ControllerFiltros import filtroFloat
from ..models.Models import Gf3003, Gf3006
from flask import session, abort, request
from ..configurations.DataBase import DB
from flask_login import login_required
from datetime import datetime, date
from ..extensions.Log import Log
from calendar import monthrange
from sqlalchemy import func
import traceback
import sys

class ControllerDashboard(HttpResponse, Log):
    """
    Classe Controller para as funções relacionadas ao dashboard
    @author - Fabio
    @tables - Gf3001, Gf3006
    @version - 1.0
    @since - 11/10/2023
    """
    
    @login_required
    def renderizaDash(self):
        try:
            valoresCalculo = self.calculaSegmentos()   
            ultimasBaixas = self.ultimasBaixas() 
            ultimosMesesSeg = self.calculoSegmentosUltimosMeses()
            
            context = {"titulo": "Dashboard", "active": "dashboard", "valoresCalculo": valoresCalculo, "ultimasBaixas": ultimasBaixas, "ultimosMesesSeg": ultimosMesesSeg}
            return self.responseRender("public/dashboard.html", context=context)

        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)
    

    @login_required
    def trocaFilial(self):
        try:
            if session["filial"] == 1: #Troca a Filial na sessão do cookie
                session["filial"] = 2
            else: 
                session["filial"] = 1
            
            return self.responseRedirect(url="dashboardBlue.dashboard")
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    def ultimasBaixas(self):
        baixas = DB.session.query(Gf3006).filter(Gf3006.m_ativo == 1).order_by(Gf3006.m_id.desc())   
        paginasBaixa = baixas.paginate(page=1, per_page=5)

        return paginasBaixa


    def calcularPorcentagemDiferenca(self, valorAntigo: float, valorNovo: float):
        valorNovo = filtroFloat(valorNovo) 
        valorAntigo = filtroFloat(valorAntigo) 

        if valorAntigo == 0 and valorNovo == 0:
            return 0
        elif valorAntigo == 0:
            return ((valorNovo - valorAntigo) / 1) * 100
        else:
            return ((valorNovo - valorAntigo) / valorAntigo) * 100
    

    def calculaSegmentos(self):
        segmentos = DB.session.query(Gf3003.s_id, Gf3003.s_abrev)
        
        valoresSeg = {}
        for seg in segmentos:

            dataAtual = datetime.now()
            dataAtual = dataAtual - relativedelta(months=1)
            ultimoDia = dataAtual.replace(day=monthrange(dataAtual.year, dataAtual.month)[1]).strftime("%Y%m%d")
            dataAtual = dataAtual.strftime("%Y%m%d")
            primeiroDia = f"{dataAtual[0:6]}01"

            somaPassado = DB.session.query(func.sum(Gf3006.m_valor))\
            .filter(Gf3006.m_dataBaixa>=primeiroDia, Gf3006.m_dataBaixa<=ultimoDia, Gf3006.m_idSegmento==seg.s_id).first()

            dataAtual = datetime.now()
            ultimoDia = dataAtual.replace(day=monthrange(dataAtual.year, dataAtual.month)[1]).strftime("%Y%m%d")
            dataAtual = dataAtual.strftime("%Y%m%d")
            primeiroDia = f"{dataAtual[0:6]}01"

            somaAtual = DB.session.query(func.sum(Gf3006.m_valor))\
            .filter(Gf3006.m_dataBaixa>=primeiroDia, Gf3006.m_dataBaixa<=ultimoDia, Gf3006.m_idSegmento==seg.s_id).first()

            porcentagem = self.calcularPorcentagemDiferenca(somaPassado[0], somaAtual[0])

            dicSeg = {
                "valor": filtroFloat(somaAtual[0]),
                "porcentagem": filtroFloat(porcentagem)
            }

            valoresSeg[f"{seg.s_abrev}"] = dicSeg

        return valoresSeg


    def calculoSegmentosUltimosMeses(self):
        segmentos = DB.session.query(Gf3003.s_id, Gf3003.s_abrev)

        valoresSeg = []
        for seg in segmentos:
            listaValor = []
            listaMeses = []
            for x in range(0, 7):
                dataAtual = date.today()
                dataAtual = dataAtual - relativedelta(months=x+1)  
                nomeMes = dataAtual.strftime("%b %y")
                ultimoDia = dataAtual.replace(day=monthrange(dataAtual.year, dataAtual.month)[1]).strftime("%Y%m%d")
                dataAtual = dataAtual.strftime("%Y%m%d")
                primeiroDia = f"{dataAtual[0:6]}01"
                
                #Query que trás todas as baixas dentro do range
                baixas = DB.session.query(func.sum(Gf3006.m_valor)) \
                .filter(Gf3006.m_dataBaixa>=primeiroDia, Gf3006.m_dataBaixa<=ultimoDia, Gf3006.m_idSegmento==seg.s_id).first()
                
                listaValor.append(filtroFloat(baixas[0]))
                listaMeses.append(nomeMes)
            
            listaValor.reverse()
            listaMeses.reverse()
            listaValor.insert(0, 0)
            listaMeses.insert(0, "")
            
            dicSeg = {
                "sigla": seg.s_abrev,
                "data": listaValor,
                "meses": listaMeses,
                "max": max(listaValor) + 100000
            }

            valoresSeg.append(dicSeg)

        return valoresSeg