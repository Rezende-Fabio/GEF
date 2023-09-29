import os
import dateutil.parser
from datetime import datetime
import locale


def get_path(nome):
    BASEDIR = os.path.dirname(os.path.realpath(nome))
    if "G:" in BASEDIR:
        BASEDIR = f"{BASEDIR}GefIII"
        return BASEDIR
    else:
        return BASEDIR


def filtroFloat(valor):
    if valor == None:
        return 0
    else:
        return float(("%.2f"%valor))


def filtroValor(valor):
    if valor == None:
        valor = 0
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        valor = locale.currency(valor, grouping=True, symbol=True)
        return ( "%s" % valor)
    else:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        valor = locale.currency(valor, grouping=True, symbol=True)
        return ( "%s" % valor)


def filtroData(date, fmt=None):
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%d/%m/%Y'
    return native.strftime(format)


def filtroTipoBaixa(tipoBaixa):
    if tipoBaixa == "BT":
        return "Baixa Tot."
    elif tipoBaixa == "BP":
        return "Baixa Parc."
    elif tipoBaixa == "DT":
        return "Dev. Tot."
    elif tipoBaixa == "DP":
        return "Dev. Parc."

    
def filtroNome(nome):
    return nome[:10]


def calculaDias(data):
    dataAtual = datetime.now().strftime("%Y%m%d")
    dataAtual = datetime.strptime(dataAtual, "%Y%m%d")
    data = datetime.strptime(data, "%Y%m%d")
    if data > dataAtual:
        return 0
    else:
        return abs((dataAtual - data).days)
    
    
def situacao(valor, saldo):
    if saldo == 0:
        return "Liquid."
    elif saldo == valor:
        return "Pendente"
    elif saldo != valor:
        return "Baixa Parc."


def filtroStatus(status):
    if status == 1:
        return "Ativo"
    else:
        return "Inativo"
    

def filtroCpf(cpfCnpj):
    if len(cpfCnpj) < 11:
        cpfCnpj = "--"
    elif len(cpfCnpj) == 11:
        cpfCnpj = cpfCnpj[0:3] + "." + cpfCnpj[3:6] + "." + cpfCnpj[6:9] + "-" + cpfCnpj[9:]
    else:
        cpfCnpj = cpfCnpj[0:3] + "." + cpfCnpj[3:6] + "." + cpfCnpj[6:8] + "/" + cpfCnpj[8:12] + "-" + cpfCnpj[12:] 
    return cpfCnpj


def filtroDataInput(date):
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%Y-%m-%d'
    return native.strftime(format) 


def filtroStatusUser(status):
    if status == 1:
        return "Sim"
    else:
        return "Não"