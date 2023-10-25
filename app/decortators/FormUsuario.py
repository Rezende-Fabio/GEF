from functools import wraps
from flask import request, Response

def validaFormUsuario(f):
    @wraps(f) 
    def wrapper(*args, **kwargs):
        form = request.form
        if form["senha"].upper().strip() != form["confSenha"].upper().strip():
            response = Response("As senhas não são iguais!", status=400)
            return response
        elif ".net" not in form["email"].lower() or "@" not in form["email"].lower():
            response = Response("Verifique o e-mail digitado!", status=400)
            return response
        
        resultado = f(*args, **kwargs)
        return resultado
    return wrapper