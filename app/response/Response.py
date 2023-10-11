from flask import flash, render_template, redirect, url_for
from typing import Optional

class Response:

    def render(self, arquivo: str, context: Optional[dict]=None, mensagem: Optional[str]=None, categoria: Optional[str]=None):
        if mensagem != None: flash(mensagem, categoria)

        if context != None: return render_template(arquivo, context=context)
        else: render_template(arquivo)


    def redirect(self, url: str, mensagem: Optional[str]=None, categoria: Optional[str]=None):
        if mensagem != None: flash(mensagem, categoria)
        
        return redirect(url_for(url))
    
    