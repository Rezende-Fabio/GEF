from ..httpResponse.HttpResponse import HttpResponse
from flask import session, abort, request, g, jsonify
from flask_login import login_required
from ..extensions.configHtml import *
from ..models.Models import Gf3002
from ..extensions.Log import Log
import traceback
import sys

class ControllerVendedor(HttpResponse, Log):
    """
    Classe Controller para as funções relacionadas aos vendedores
    @author - Fabio
    @tables - Gf3002
    @version - 1.0
    @since - 18/10/2023
    """

    @login_required
    def renderListaVendedores(self) -> HttpResponse:
        try:
            context = {"active": "vendedor", "titulo": "Lista de Vendedores"}
            return self.responseRender(arquivo="vendedor/listaVendedores.html", context=context)

        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def renderConsultarVendedor(self, idVend: str) -> HttpResponse:
        try:
            vendedor = Gf3002.query.get(idVend)
            context = {"vendedor": vendedor}
            return self.responseRender("vendedor/corpoModalVisuVend.html", context=context)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)

    
    @login_required
    def atulizarBaseVendedor(self) -> HttpResponse:
        try:
            return self.responseEventStream(g.integracao.integraVendedor())
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def atulizarBaseVendedorRedirect(self) -> HttpResponse:
        try:
            self.geraLogDiario("Atulizou a base de Vendedores", session["usuario"]["usuario"], session["filial"])
            return self.responseRedirect(url="vendedorBlue.renderListaVendedores", mensagem="Base atualizada com sucesso!", categoria="success")
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def consultarVendedores(self) -> HttpResponse:
        try:
            #Query que trás todos os vendedores
            vendedores = Gf3002.query.order_by(Gf3002.v_id)
            listaVend = []
            for vend in vendedores:
                dictVend = {
                    "cod": vend.v_id, 
                    "nome": vend.v_nome, 
                    "cpfCnpj": filtroCpf(vend.v_cpfcnpj), 
                    "tel": vend.v_telefone, 
                    "status": "ATIVO" if vend.v_ativo else "INATIVO"
                }
                listaVend.append(dictVend)

            return self.responseJson(body=listaVend, status=200)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def pesquisarVendedoresAutocomplete(self, pesquisa: str) -> HttpResponse:
        try:
            if pesquisa.isdigit(): #Verifica se o que foi enviado é número
                #Query que consulta os nomes de acordo com o código do vendedor
                vendedores = Gf3002.query.filter(Gf3002.v_id.like(f"%{pesquisa}%"), Gf3002.v_ativo==1)
            else:
                #Query que consulta os nomes de acordo com o nome do vendedor
                vendedores = Gf3002.query.filter(Gf3002.v_nome.like(f"%{pesquisa}%"), Gf3002.v_ativo==1) 
            listaVend = [vend.as_dict() for vend in vendedores]
            return jsonify(listaVend)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)

    
    @login_required
    def verificarVendedor(self, idVend: str) -> HttpResponse:
        try:
            vendedor = Gf3002.query.filter(Gf3002.v_id==idVend).first()
            if vendedor:
                return self.responseJson(status=200)
            else:
                return self.responseJson(status=400)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)
        