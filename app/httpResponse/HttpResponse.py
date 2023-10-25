from flask import flash, render_template, redirect, url_for, Response
from typing import Optional
from typing import Callable
import json

class HttpResponse:
    """
    Classe para os tipos de resposta do sistema
    @author - Fabio
    @version - 1.0
    @since - 06/10/2023
    """

    def responseRender(self, arquivo: str, context: Optional[dict]=None, mensagem: Optional[str]=None, categoria: Optional[str]=None):
        if mensagem != None: flash(mensagem, categoria)

        if context != None: return render_template(arquivo, context=context)
        else: return render_template(arquivo)


    def responseRedirect(self, url: str, mensagem: Optional[str]=None, categoria: Optional[str]=None):
        if mensagem != None: flash(mensagem, categoria)
        
        return redirect(url_for(url))
    

    def responseJson(self, status: int, body: Optional[dict]=None) -> Response:
        if body:
            response = Response(json.dumps(body), status=status, mimetype="application/json")
        else:
            response = Response(status=status)

        return response
    

    def responseJsonMessage(self, status: int, body: Optional[dict]=None, mensagem: Optional[str]=None, categoria: Optional[str]=None) -> Response:
        if mensagem != None: flash(mensagem, categoria)
        if body:
            response = Response(json.dumps(body), status=status, mimetype="application/json")
        else:
            response = Response(status=status)

        return response
    

    def responseEventStream(self, funcao:  Callable[[], None]) -> Response:
        response = Response(funcao, mimetype='text/event-stream')

        return response

    