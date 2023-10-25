from functools import wraps
from flask import request, Response

def validaFormBaixa(f):
    @wraps(f) 
    def wrapper(*args, **kwargs):
        form = request.form
        if float(form["valorBaixa"]) > float(form["valorParcela"]):
            response = Response("Valor da baixa maior do que o valor da parcela!", status=400)
            return response
        elif float(form["valorBaixa"]) > float(form["valorSaldo"]):
            response = Response("Valor da baixa maior do que o valor do saldo!", status=400)
            return response
        
        resultado = f(*args, **kwargs)
        return resultado
    return wrapper