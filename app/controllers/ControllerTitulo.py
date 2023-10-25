from ..models.Models import Gf3004, Gf3001, Gf3002, Gf3003, Gf3006
from ..httpResponse.HttpResponse import HttpResponse
from dateutil.relativedelta import relativedelta
from flask import request, abort, session
from ..configurations.DataBase import DB
from flask_login import login_required
from .ControllerFiltros import *
from ..extensions.Log import Log
from sqlalchemy import func
import traceback
import sys

class ControllerTitulo(HttpResponse, Log):
    """
    Classe Controller para as funções relacionadas aos títulos
    @author - Fabio
    @tables - Gf3004, Gf3001, Gf3002, Gf3003, Gf3006
    @version - 1.0
    @since - 23/10/2023
    """

    @login_required
    def renderListaTitulos(self) -> HttpResponse:
        try:    
            context = {"active": "titulo", "titulo": "Lista de Títulos"}
            return self.responseRender(arquivo="titulo/listaTitulos.html", context=context)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)

    #Rota para preencher a lista de titulos
    @login_required
    def consultarTitulos(self) -> HttpResponse:
        try:    
            dataAtual = datetime.now()
            dataAtual = dataAtual - relativedelta(years=1)
            dataAtual = dataAtual.strftime("%Y")
            
            #Query que trás todos os títulos exeto os excluidos
            titulos = DB.session.query(Gf3004.t_dataLanc, Gf3004.t_idCliente, Gf3004.t_idVendedor,Gf3004.t_numDoc, 
                                       func.count(Gf3004.t_numParcela).label('parcelas'), func.sum(Gf3004.t_valor).label('total'), 
                                       Gf3001.c_razaosocial.label('cliente'), Gf3001.c_cpfcnpj.label('cpfcnpjCli'), Gf3002.v_cpfcnpj.label("cpfcnpjVend"), 
                                       Gf3004.t_docRef, Gf3003.s_abrev)\
            .filter(Gf3004.t_ativo == True, Gf3004.t_filial == session["filial"], Gf3004.t_dataLanc >= dataAtual)\
            .join(Gf3003, Gf3003.s_id == Gf3004.t_idSegmento)\
            .join(Gf3001, Gf3004.t_idCliente==Gf3001.c_id)\
            .join(Gf3002, Gf3004.t_idVendedor==Gf3002.v_id)\
            .group_by(Gf3004.t_dataLanc, Gf3004.t_idCliente, Gf3001.c_razaosocial, Gf3004.t_idVendedor, Gf3004.t_numDoc, Gf3003.s_abrev).order_by(Gf3004.t_dataLanc)

            listaTitulos = []
            for x in titulos:
                listaTitulos.append({"ref": x.t_docRef, "doc": x.t_numDoc, "par": x.parcelas, "cli": filtroNome(x.cliente), "abrev": x.s_abrev, "lanc": filtroData(x.t_dataLanc), "total":filtroValor(x.total), "cpfcnpjCli":x.cpfcnpjCli, "cpfcnpjVend":x.cpfcnpjVend})
            return self.responseJson(body=listaTitulos, status=200)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)

    
    @login_required
    def renderConsultarTitulo(self, doc: int) -> HttpResponse:
        try:    
            tituloValores = DB.session.query( func.count(Gf3004.t_numParcela).label('parcelas'), func.sum(Gf3004.t_valor).label('valorTotal'))\
            .filter(Gf3004.t_ativo==True, Gf3004.t_numDoc==doc)\
            .group_by(Gf3004.t_idCliente, Gf3004.t_idVendedor, Gf3004.t_idSegmento).first()

            titulo = Gf3004.query.filter(Gf3004.t_numDoc==doc).first()

            #Query que trás todas a parcelas separadas do documento
            parcelas = DB.session.query(Gf3004.t_dataVenc, Gf3004.t_valor, Gf3004.t_numParcela, Gf3004.t_status)\
            .filter(Gf3004.t_numDoc==doc)\
            .order_by(Gf3004.t_numParcela)

            context = {"titulo": titulo, "tituloValores": tituloValores, "parcelas": parcelas} #Dicionário contendo as variáveis para utilizar no template
            return self.responseRender(arquivo="titulo/corpoModalVisuTi.html", context=context)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def consultarTitulo(self, doc: int) -> HttpResponse:
        try:
            titulo = Gf3004.query.filter(Gf3004.t_numDoc==doc).first()
            if titulo:
                return self.responseJson(body=titulo.toJson(), status=200)
            else:
                return self.responseJson(body=titulo.toJson(), status=200)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def renderCadastrarTitulo(self) -> HttpResponse:
        try:
            #Query que trás os segmentos de acordo com a filial logada
            segmentos = Gf3003.query.filter(Gf3003.s_filial == session["filial"])
    
            #Query que trás o último número do documento cadastrado
            numDoc = Gf3004.query.order_by(Gf3004.t_numDoc.desc()).first()
            
            data = datetime.today().strftime("%Y-%m-%d")
            context = {"titulo": "Inclusão de Título", "data": data, "numDoc": numDoc, "segmentos": segmentos, "active": "titulo", "titulo": "Inclusão de Título"}
            return self.responseRender(arquivo="titulo/cadTitulo.html", context=context)

        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)

    
    @login_required
    def inserirTitulo(self) -> HttpResponse:
        try:
            form = request.form
            parcelas = int(form["parcelas"])
            for x in range(0, parcelas):
                idCliente = list(form["cliente"].split())
                idVendedor = list(form["vendedor"].split())
                parcela = float(form[f"valor{x+1}"])
                dataVenc = form[f"parcela{x+1}"].replace("-", "")
                
                titulo = Gf3004(t_numDoc=form["numDoc"],
                                t_numParcela=x+1,
                                t_valor=parcela,
                                t_dataLanc=form["dataLanc"].replace("-", ""),
                                t_dataVenc=dataVenc,
                                t_idCliente=idCliente[0],
                                t_idVendedor=idVendedor[0],
                                t_saldo=parcela,
                                t_status=True,
                                t_docRef=form["docRef"],
                                t_idSegmento=form["segmento"],
                                t_filialOri=int(session["filial"]),
                                t_filial=int(form["filialSelc"]),
                                t_ativo=True,
                                t_comissao =float(form["comissao"])
                                )
                
                DB.session.add(titulo)
            
            DB.session.commit()
            self.geraLogDiario("Inseriu um Título", session["usuario"]["usuario"], session["filial"], f"Documento: {request.form['numDoc']}") #Gera log informando que foi feita uma inserção de título   
            return self.responseJsonMessage(status=204, mensagem="Título cadastrado com sucessso!", categoria="success")
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def renderEditarTitulo(self, doc: int) -> HttpResponse:
        try:
            if self.verificarExisteBaixa(doc):
                return self.responseRedirect(url="tituloBlue.renderListaTitulos", mensagem=f"Título {doc} não pode ser editado, pois existem baixa(s), efetue o estorno(s) para editar!!", categoria="warning")
            else:
                tituloValores = DB.session.query( func.count(Gf3004.t_numParcela).label('parcelas'), func.sum(Gf3004.t_valor).label('valorTotal'))\
                .filter(Gf3004.t_ativo==True, Gf3004.t_numDoc==doc)\
                .group_by(Gf3004.t_idCliente, Gf3004.t_idVendedor, Gf3004.t_idSegmento).first()

                titulo = Gf3004.query.filter(Gf3004.t_numDoc==doc).first()

                parcelas = DB.session.query(Gf3004.t_dataVenc, Gf3004.t_valor, Gf3004.t_numParcela).filter(Gf3004.t_numDoc==doc).order_by(Gf3004.t_numParcela)

                context = {"tituloDoc": titulo, "tituloValores": tituloValores, "parcelas": parcelas, "titulo": "Atualização de Título"}
                return self.responseRender(arquivo="titulo/editTitulo.html", context=context)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)

    @login_required
    def editarTitulo(self, doc: int) -> HttpResponse:
        try:
            form = request.form
            for x in range(0, int(form["parcelas"])):
                campos = {
                    "t_dataVenc": form[f"parcela{x+1}"].replace("-", ""),
                    "t_comissao": form["comissao"]
                }

                Gf3004.query.filter(Gf3004.t_numDoc==doc, Gf3004.t_numParcela==x+1).update(campos)
            
            DB.session.commit()
            self.geraLogDiario("Alterou um Título", session["usuario"]["usuario"], session["filial"], f"Documento: {doc}") #Gera log informando que foi feita alteração no documento
            return self.responseJsonMessage(status=204, mensagem=f"Título {doc} foi atualizado com sucesso!", categoria="success")
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)
        
    
    @login_required
    def excluirTitulo(self, doc: int) -> HttpResponse:
        try:    
            if self.verificarExisteBaixa(doc):
                return self.responseJsonMessage(status=409, mensagem=f"Título {doc} não pode ser excluido, pois existem baixa(s), efetue o estorno(s) para excluir!!", categoria="danger")
            else:
                campos = {
                    "t_ativo": False
                }
                Gf3004.query.filter(Gf3004.t_numDoc==doc).update(campos)
                DB.session.commit()
                self.geraLogDiario("Exclusão de Título", session["usuario"]["usuario"], session["filial"], f"Documento: {doc}")
                return self.responseJsonMessage(status=200, mensagem=f"Título {doc} excluido com sucesso!", categoria="success")
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)

    #Rota para verificar se o documento de referencia já existe na tabela
    @login_required
    def verificarDocRefTitulo(self, docRef: str, filial: int) -> HttpResponse:
        try:
            doc = Gf3004.query.filter(Gf3004.t_docRef==docRef, Gf3004.t_ativo==True, Gf3004.t_filialOri==filial).first()
            if doc:
                return self.responseJson(status=204)
            else:
                return self.responseJson(status=404)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def autocompleteIdCliente(self, idCli: str) -> HttpResponse:
        try:
            #Query que trás todos os documentos que o cliente tem no sistema
            docs = Gf3004.query.filter(Gf3004.t_idCliente==idCli).group_by(Gf3004.t_docRef).all()
            listaDocs = [n.as_dict() for n in docs]
            return self.responseJson(body=listaDocs, status=200)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)

    #Rota para verificar se o campo documento referência no cadastro de devolução está correto
    @login_required
    def verificaDocRefCliente(self, docRef: str, idCli: str) -> HttpResponse:
        try:
            #Query que verifica se o documento de referência que foi passado existe para o cliente passado
            doc = Gf3004.query.filter(Gf3004.t_docRef==docRef, Gf3004.t_idCliente==idCli).first()
            if doc:
                return self.responseJson(status=204)
            else:
                return self.responseJson(status=404)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    def verificarExisteBaixa(self, doc: int) -> bool:
        baixa = Gf3006.query.filter(Gf3006.m_numDoc==doc, Gf3006.m_ativo==1).first()

        if baixa: return True
        else: return False