from ..httpResponse.HttpResponse import HttpResponse
from flask import abort, request, g, session
from flask_login import login_required
from ..extensions.configHtml import *
from ..models.Models import Gf3001
from ..extensions.Log import Log
import traceback
import sys

class ControllerCliente(HttpResponse, Log):
    """
    Classe Controller para as funções relacionadas aos clientes
    @author - Fabio
    @tables - Gf3001
    @version - 1.0
    @since - 19/10/2023
    """

    @login_required
    def renderListaClientes(self) -> HttpResponse:
        try:
            context = {"active": "cliente", "titulo": "Lista de Clientes"}
            return self.responseRender(arquivo="cliente/listaClientes.html", context=context)

        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def renderConsultaCliente(self, idCli: str) -> HttpResponse:
        cliente = Gf3001.query.get(idCli)
        context = {"cliente": cliente}
        return self.responseRender(arquivo="cliente/corpoModalVisuCli.html", context=context)
    

    @login_required
    def atulizarBaseCliente(self) -> HttpResponse:
        try:
            return self.responseEventStream(g.integracao.integraClientes())
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)

    
    @login_required
    def atulizarBaseClienteRedirect(self) -> HttpResponse:
        try:
            self.geraLogDiario("Atulizou a base de Clientes", session["usuario"]["usuario"], session["filial"])
            return self.responseRedirect(url="clienteBlue.renderListaClientes", mensagem="Base atualizada com sucesso!", categoria="success")
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)

        
    @login_required
    def consultarClientes(self) -> HttpResponse:
        try:
            #Query que trás todos os clientes
            clientes = Gf3001.query.order_by(Gf3001.c_id)
            listaCli = []
            for cli in clientes:
                dictCli = {
                    "cod": cli.c_id, 
                    "loja": cli.c_loja, 
                    "nome": cli.c_razaosocial, 
                    "cpfCnpj": filtroCpf(cli.c_cpfcnpj), 
                    "status": "ATIVO" if cli.c_ativo else "INATIVO"
                }
                listaCli.append(dictCli)

            return self.responseJson(body=listaCli, status=200)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def pesquisarClientesAutocomplete(self, pesquisa: str) -> HttpResponse:
        try:
            if pesquisa.isdigit(): #Verifica se o que foi enviado é número
                #Query que consulta os nomes de acordo com o código do cliente
                clientes = Gf3001.query.filter(Gf3001.c_id.like(f"%{pesquisa}%"), Gf3001.c_ativo==1)
            else:
                #Query que consulta os nomes de acordo com o nome do cliente
                clientes = Gf3001.query.filter(Gf3001.c_razaosocial.like(f"%{pesquisa}%"), Gf3001.c_ativo==1) 
            listaCli = [cli.as_dict() for cli in clientes]
            return self.responseJson(body=listaCli, status=200)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)

    
    @login_required
    def verificarCliente(self, idCli: str) -> HttpResponse:
        try:
            cliente = Gf3001.query.filter(Gf3001.c_id==idCli).first()
            if cliente:
                return self.responseJson(status=200)
            else:
                return self.responseJson(status=400)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)