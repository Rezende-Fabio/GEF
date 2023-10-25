from ..models.Models import *
from datetime import datetime


def consultaAtraso():
    dataAtual = datetime.today().strftime("%Y%m%d") 
    qtdeAtraso = Gf3004.query.filter(Gf3004.t_dataVenc<dataAtual, Gf3004.t_ativo==True, Gf3004.t_status==True).count()

    return qtdeAtraso