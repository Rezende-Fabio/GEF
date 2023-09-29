from flask import Blueprint
import dateutil.parser
from datetime import datetime
import locale

filtrosBlue = Blueprint("filtrosBlue", __name__)

#Filtro para Data input
@filtrosBlue.app_template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%Y-%m-%d'
    return native.strftime(format) 

#Filtro para Data lista
@filtrosBlue.app_template_filter('data')
def _jinja2_filter_datetime(date, fmt=None):
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%d/%m/%Y'
    return native.strftime(format)

#Filtro para CPF/CNPJ
@filtrosBlue.app_template_filter('cpfCnpj')
def _jinja2_filter_cpf(cpfCnpj, fmt=None):
    if len(cpfCnpj) < 11:
        cpfCnpj = "--"
    elif len(cpfCnpj) == 11:
        cpfCnpj = cpfCnpj[0:3] + "." + cpfCnpj[3:6] + "." + cpfCnpj[6:9] + "-" + cpfCnpj[9:]
    else:
        cpfCnpj = cpfCnpj[0:3] + "." + cpfCnpj[3:6] + "." + cpfCnpj[6:8] + "/" + cpfCnpj[8:12] + "-" + cpfCnpj[12:] 
    return cpfCnpj

#Filtro para CEP
@filtrosBlue.app_template_filter('cep')
def _jinja2_filter_cep(cep, fmt=None):
    if cep == "--":
        cep = cep
    else:
        cep = cep[0:5] + "-" + cep[5:]
    return cep

#Filtro para tittulo vencido
@filtrosBlue.app_template_filter('vencido')
def _jinja2_filter_vencido(data, fmt=None):
    data = dateutil.parser.parse(data)
    native = data.replace(tzinfo=None)
    format='%Y-%m-%d'
    data = native.strftime(format)
    dataAtual = datetime.now().strftime("%Y-%m-%d")
    if data < dataAtual:
        return False
    else:
        return True
    
#Filtro para valores
@filtrosBlue.app_template_filter('float')
def _jinja2_filter_float(valor, fmt=None):
    return float("%.2f"%valor)

#Filtro para valores em real
@filtrosBlue.app_template_filter('real')
def _jinja2_filter_real(valor, fmt=None):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    valor = locale.currency(valor, grouping=True, symbol=True)
    return ( "%s" % valor)

#Filtro para status
@filtrosBlue.app_template_filter('status')
def _jinja2_filter_status(status, fmt=None):
    if status == 1:
        retorno = "Ativo"
    else:
        retorno = "Inativo"
    return retorno

#Filtro para nome
@filtrosBlue.app_template_filter('nome')
def _jinja2_filter_nome(nome, fmt=None):
    return nome[:10]

#Filtro para o tipo de baixa
@filtrosBlue.app_template_filter('tpBixa')
def _jinja2_filter_baixa(tipoBaixa, fmt=None):
    if tipoBaixa == "BT":
        return "Baixa Tot."
    elif tipoBaixa == "BP":
        return "Baixa Parc."
    elif tipoBaixa == "DT":
        return "Dev. Tot."
    elif tipoBaixa == "DP":
        return "Dev. Parc."





