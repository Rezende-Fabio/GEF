from dateutil.relativedelta import relativedelta
from ..response.Response import Response
from ..configurations.DataBase import DB
from calendar import monthrange
from ..models.Models import *
from datetime import datetime
from sqlalchemy import func


class ControllerDashboard(Response):
    """
    Classe Controller para as funções relacionadas ao login do sistema
    @author - Fabio
    @version - 1.0
    @since - 11/10/2023
    """

    def calcularPorcentagemDiferenca(self, valorAntigo: float, valorNovo: float):
        if valorNovo != None: valorNovo = round(valorNovo, 2) 
        else: valorNovo = 0

        if valorAntigo != None: valorAntigo = round(valorAntigo, 2) 
        else: valorAntigo = 0

        if valorAntigo == 0 and valorNovo == 0:
            return 0
        else:
            return ((valorNovo - valorAntigo) / valorAntigo) * 100
    

    def efetuaCalculos(self):
        valoresCalculo = self.calculaSegmentos()    
        context = {"titulo": "Dashboard", "active": "dashboard", "valoresCalculo": valoresCalculo}
        return self.render("public/dashboard.html", context=context)


    def calculaSegmentos(self):
        segmentos = DB.session.query(Gf3003.s_id, Gf3003.s_abrev)
        
        valoresSeg = {}
        for seg in segmentos:

            dataAtual = datetime.now()
            dataAtual = dataAtual - relativedelta(months=1)
            ultimoDia = dataAtual.replace(day=monthrange(dataAtual.year, dataAtual.month)[1]).strftime("%Y%m%d")
            dataAtual = dataAtual.strftime("%Y%m%d")
            primeiroDia = f"{dataAtual[0:6]}01"

            somaPassado = DB.session.query(func.sum(Gf3004.t_valor)).filter(Gf3004.t_dataVenc>=primeiroDia, Gf3004.t_dataVenc<=ultimoDia, Gf3004.t_status==False, Gf3004.t_ativo==True, Gf3004.t_segmento==seg.s_id).first()

            dataAtual = datetime.now()
            ultimoDia = dataAtual.replace(day=monthrange(dataAtual.year, dataAtual.month)[1]).strftime("%Y%m%d")
            dataAtual = dataAtual.strftime("%Y%m%d")
            primeiroDia = f"{dataAtual[0:6]}01"

            somaAtual = DB.session.query(func.sum(Gf3004.t_valor)).filter(Gf3004.t_dataVenc>=primeiroDia, Gf3004.t_dataVenc<=ultimoDia, Gf3004.t_status==False, Gf3004.t_ativo==True, Gf3004.t_segmento==seg.s_id).first()

            porcentagem = self.calcularPorcentagemDiferenca(somaPassado[0], somaAtual[0])

            dicSeg = {
                "valor": round(somaAtual[0], 2) if somaAtual[0] else 0,
                "porcentagem": round(porcentagem, 2)
            }

            valoresSeg[f"{seg.s_abrev}"] = dicSeg

        return valoresSeg