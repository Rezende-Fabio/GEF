import os
import dateutil.parser
from datetime import datetime
import locale


def filtroFloat(valor):
    if valor == None:
        return 0
    else:
        return round(valor, 2)
    

def filtroNome(nome):
    return nome[:10]


def filtroData(date, fmt=None):
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%d/%m/%Y'
    return native.strftime(format)


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