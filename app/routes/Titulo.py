from flask import render_template, request, redirect, flash, session, jsonify
from sqlalchemy import func, update
from app import app
from ..bd.models import *
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from ..extensions.configHtml import *
from ..extensions.logs import Logger
from sqlalchemy import or_
import sys
from ..extensions.veriaveis import *

###################################
# Rotas relacionadas aos titulos
# TABELA DE TITULOS GF3004
###################################


#Rota para Tela de listagem de titulos
@app.route("/lista-titulos", methods=["GET", "POST"])
def listaTitulos():
    ###################################################################################################
    # Função que renderiza a tela de listagem de títulos.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("titulo/listaTitulos.html") = Redireciona para listagem de títulos;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            return render_template("titulo/listaTitulos.html")
        
        else:
           return redirect("/") 
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")
    
#Rota para modal de confirmação para excluir titulo e para vizualização do título
@app.route("/lista-titulos/view/<doc>")
@app.route("/lista-titulos/<doc>")
def popupTitulo(doc):
    ###################################################################################################
    # Função que exibe modal para a vizualização dos dados do título quando a url tem o "view", quando
    # não tem, verifica se exixtem baixas nesse documento, se tiver retorna que o título não pode ser
    # excluido, se não tiver exibe modal para confirmação da exclusão.
    
    # PARAMETROS:
    #   doc = Número do documento que foi selecionado.
    
    # RETORNOS:
    #   return render_template("titulo/listaTitulos.html", contexto=contexto) = Redireciona para listagem
    #     mostrando um modal com a insformações do título;
    #   return render_template("titulo/listaTitulos.html") = Redireciona para listagem de títulos com a
    #     mensagem de que o título não pode ser excluido;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            if "view" in request.url:
                conexao = Gf3004 #Conexão com a tabela de títulos
                conexao2 = Gf3001 #Conexão com a tabela de clientes
                conexao3 = Gf3002 #Conexão com a tabela de vendedores
                conexao4 = Gf3003 #Conexão com a tabela de segmentos
                #Query que trás o título de acordo com número do documento que foi passado
                titulo = conexao.query.filter_by(t_numDoc=doc).first()
                #Query que trás o cliente e vendedor do documento
                segCliVend = db.session.query(conexao.t_idCliente, conexao.t_idVendedor, func.count(conexao.t_numParcela).label('parcelas'), func.sum(conexao.t_valor).label('valorTotal'), conexao4.s_abrev, conexao2.c_razaosocial, conexao3.v_nome).filter(conexao.t_ativo == 1, conexao.t_numDoc == doc).join(conexao4, conexao4.s_id == conexao.t_segmento).join(conexao2, conexao2.c_id == conexao.t_idCliente).join(conexao3, conexao3.v_id == conexao.t_idVendedor).group_by(conexao.t_idCliente, conexao.t_idVendedor, conexao4.s_abrev)
                #Query que trás todas a parcelas separadas do documento
                parcelas = db.session.query(conexao.t_dataVenc, conexao.t_valor, conexao.t_numParcela, conexao.t_status).filter(conexao.t_numDoc == doc).order_by(conexao.t_numParcela)
                contexto = {"aviso": 2, "titulo": titulo, "segCliVend": segCliVend, "parcelas": parcelas} #Dicionário contendo as variáveis para utilizar no template
                return render_template("titulo/listaTitulos.html", contexto=contexto)
            
            else:
                conexao = Gf3004 #Conexão com a tabela de títulos
                conexao2 = Gf3001 #Conexão com a tabela de clientes
                conexao3 = Gf3002 #Conexão com a tabela de vendedores
                conexao4 = Gf3003 #Conexão com a tabela de segmentos
                conexao5 = Gf3006 #Conexão com a tabela de movimentos
                #Query que trás o título de acordo com número do documento que foi passado
                titulo = conexao.query.filter_by(t_numDoc=doc).first()
                #Query que verifica se o documento tem baixa
                baixa = conexao5.query.filter(conexao5.m_numDoc==doc, conexao5.m_ativo==1).first()
                    
                if baixa:
                    #flash(f"Título {doc} não pode ser excluido, pois existem baixa(s)!") 
                    flash(f"Título {doc} não pode ser excluido, pois existem baixa(s), efetue o estorno(s) para excluir!!") #Mensagem para ser exibida no Front
                    return redirect("/lista-titulos")
                else:
                    contexto = {"aviso": 1, "titulo": titulo} #Dicionário contendo as variáveis para utilizar no template
                    return render_template("titulo/listaTitulos.html", contexto=contexto)

        else:
            return redirect("/")

    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")

#Rota para Tela de cadastro de titulos
@app.route("/cad-titulo")
def cadTitulo():
    ###################################################################################################
    # Função que renderiza a tela de cadastro de título, passado para o template os segmentos de acordo 
    # com a filial logada, o novo número do documento e a data atual.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("titulo/cadTitulo.html", contexto=contexto) = Redireciona para cadastro
    #     do título passando os segmentos, último número do documento e data atual;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            conexao = Gf3003 #Conexão com a tabela de segmentos
            #Query que trás os segmentos de acordo com a filial logada
            segmentos = conexao.query.filter(conexao.s_filial == session["filial"])
            
            conexao = Gf3004 #Conexão com a tabela de títulos
            #Query que trás o último número do documento cadastrado
            numDoc = conexao.query.order_by(conexao.t_numDoc.desc()).first()
            
            data = datetime.today().strftime("%Y-%m-%d")
            contexto = {"titulo": "Inclusão de Título", "action": "/insert-titulo", "botao": "Gravar", "data": data, "numDoc": numDoc, "segmentos": segmentos} #Dicionário contendo as variáveis para utilizar no template
            return render_template("titulo/cadTitulo.html", contexto=contexto)
        
        else:
            return redirect("/")
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")

#Rota para inserir titulos
@app.route("/insert-titulo", methods=["GET", "POST"])
def insertTitulo():
    ###################################################################################################
    # Função que insere o título no banco.
    
    # PARAMETROS:
    #   request.form["parcelas"] = Número de parcelas informadas no input;
    #   request.form["cliente"] = Cliente informado no input;
    #   request.form["vendedor"] = Vendedor informado no input;
    #   request.form[f"valor{x+1}"] = Valor da percala informado nos inputs de acordo com o número de parcelas;
    #   request.form[f"parcela{x+1}"] = Data de vencimento nos inputs de acordo com o número de parcelas;
    #   request.form["numDoc"] = Número do documento que o sistema autoincrementa;
    #   request.form["dataLanc"] = Data de lançamento que foi informada no input;
    #   request.form["docRef"] = Número do documento de referência que foi infromado no input;
    #   request.form["segmento"] = Id do segmento que foi informado no input;
    #   request.form["filialSelc"] = Filial que foi selecionada no input;
    #   request.form["comissao"] = Comissão que foi informada no input;
    
    # RETORNOS:
    #   return redirect("/lista-titulos") = Redireciona para listagem de títulos com a mensagem que o
    #     título foi cadastrado com sucesso;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            if request.method == "POST":
                parcelas = int(request.form["parcelas"])
                for x in range(0, parcelas):
                    idCliente = list(request.form["cliente"].split())
                    idVendedor = list(request.form["vendedor"].split())
                    parcela = float(request.form[f"valor{x+1}"])
                    dataVenc = request.form[f"parcela{x+1}"].replace("-", "")
                    
                    titulo = Gf3004(t_numDoc=request.form["numDoc"],
                                    t_numParcela=x+1,
                                    t_valor=parcela,
                                    t_dataLanc=request.form["dataLanc"].replace("-", ""),
                                    t_dataVenc=dataVenc,
                                    t_idCliente=idCliente[0],
                                    t_idVendedor=idVendedor[0],
                                    t_saldo=parcela,
                                    t_status=1,
                                    t_docRef=request.form["docRef"],
                                    t_segmento=request.form["segmento"],
                                    t_filialOri=int(session["filial"]),
                                    t_filial=int(request.form["filialSelc"]),
                                    t_ativo=1,
                                    t_comissao =float(request.form["comissao"])
                                    )
                    
                    db.session.add(titulo)
                    db.session.commit()
                    
                flash(f"Título cadastrado com sucessso!") #Mensagem para ser exibida no Front
                Logger.log("Inserção de Título", session["usuario_logado"], session["filial"], f"Documento: {request.form['numDoc']}") #Gera log informando que foi feita uma inserção de título   
                return redirect("/lista-titulos")
        else:
            return redirect("/")
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")

#Rota para editar titulo
@app.route("/editar-titulo/<doc>", methods=["GET", "POST"])
def editarTitulo(doc):
    ###################################################################################################
    # Função que verifica se o documento que foi selcionado não existem baixas, se existir retorna que
    # o docuemnto não pode ser editado, se não existir ele renderiza a tela para modicação do documento
    # e se via metodo POST ele insere a(s) alterações no banco.
    
    # PARAMETROS:
    #   doc = Número do documento que foi selecionado.
    
    # RETORNOS:
    #   return render_template("titulo/editTitulo.html", contexto=contexto) = Redireciona para edição
    #     do título passando os segmentos, último número do documento e data atual;
    #   return redirect("/lista-titulos") = Redireciona para a listagem de títulos podendo ter duas mensagens
    #     não pode ser editado ou cadatrado com sucesso.
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            conexao = Gf3004 #Conexão com a tabela de títulos
            conexao2 = Gf3003 #Conexão com a tabela de segmentos
            conexao3 = Gf3001 #Conexão com a tabela de clientes
            conexao4 = Gf3002 #Conexão com a tabela de vendedores
            conexao5 = Gf3006 #Conexão com a tabela de movimentos
            #Quey que trás o título de acordo com documento passado
            titulo = conexao.query.filter_by(t_numDoc=doc).first()
            #Query que verifica se o existem baixas no documento
            baixa = conexao5.query.filter(conexao5.m_numDoc==doc, conexao5.m_ativo==1).first()
            
            if request.method == "POST":
                for x in range(0, int(request.form["parcelas"])):
                    titulo = conexao.query.filter_by(t_numDoc=doc, t_numParcela=x+1).first()
                    titulo.t_dataVenc = request.form[f"parcela{x+1}"].replace("-", "")
                    titulo.t_comissao = request.form["comissao"]
                db.session.commit()
                flash(f"Título {titulo.t_numDoc} foi atualizado com sucesso!") #Mensagem para ser exibida no Front
                Logger.log("Alteração de Título", session["usuario_logado"], session["filial"], f"Documento: {doc}") #Gera log informando que foi feita alteração no documento
                return redirect("/lista-titulos")
            
            else:
                if baixa:
                    flash(f"Título {doc} não pode ser editado, pois existem baixa(s), efetue o estorno(s) para editar!!")  #Mensagem para ser exibida no Front
                    return redirect("/lista-titulos")
                
                else:
                    #Query que trás o cliente e vendedor do documento
                    segCliVend = db.session.query(conexao.t_idCliente, conexao.t_idVendedor, func.count(conexao.t_numParcela).label('parcelas'), func.sum(conexao.t_valor).label('valorTotal'), conexao2.s_abrev, conexao3.c_razaosocial, conexao4.v_nome).filter(conexao.t_ativo == 1, conexao.t_numDoc == doc).join(conexao2, conexao2.s_id == conexao.t_segmento).join(conexao3, conexao3.c_id == conexao.t_idCliente).join(conexao4, conexao4.v_id == conexao.t_idVendedor).group_by(conexao.t_idCliente, conexao.t_idVendedor, conexao2.s_abrev)
                    #Query que trás todas a parcelas separadas do documento
                    parcelas = db.session.query(conexao.t_dataVenc, conexao.t_valor, conexao.t_numParcela).filter(conexao.t_numDoc == doc).order_by(conexao.t_numParcela)
                    contexto = {"titulo": titulo, "segCliVend": segCliVend, "parcelas": parcelas} #Dicionário contendo as variáveis para utilizar no template
                    return render_template("titulo/editTitulo.html", contexto=contexto)
                
        else:
            return redirect("/")
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")    

#Rota para a exclusão lógica do titulo
@app.route("/deletar-titulo/<doc>")
def deleteTitulo(doc):
    ###################################################################################################
    # Função que efetua o delete lógico do documento.
    
    # PARAMETROS:
    #   doc = Número do documento que foi selecionado.
    
    # RETORNOS:
    #   return redirect("/lista-titulos") = Redireciona para listagem de títulos com a mensagem de foi
    #     foi excluido com sucesso;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            conexao = Gf3004 #Conexão com a tabela de títulos
            titulos = conexao.query.filter_by(t_numDoc=doc)
            for titulo in titulos:
                titulo.t_ativo = 0     
            db.session.commit()
            flash(f"Título {doc} excluido com sucesso!") #Mensagem para ser exibida no Front
            Logger.log("Exclusão de Título", session["usuario_logado"], session["filial"], f"Documento: {doc}") #Gera log informando que o documento foi esxcluido
            return redirect("/lista-titulos")

        else:
            return redirect("/")
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")  
    
#Rota para autocomplete na tela de cadatro de Devolução
@app.route("/doc-ref/<idCli>")
def docRefCli(idCli):
    ###################################################################################################
    # API que consulta os documentos de refência do que clinete que foi passado, para validação no 
    # cadatro de devolução.
    
    # PARAMETROS:
    #   idCli = Id do cliente que foi passado.
    
    # RETORNOS:
    #   return jsonify(lista) = Retorna Json com a lista de documentos de referência do clinete;
    #   return jsonify("Error") = Retorna Json caso ocorra um erro.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            conexao = Gf3004 #Conexão com a tabela de títulos
            #Query que trás todos os documentos que o cliente tem no sistema
            docs = conexao.query.filter(conexao.t_idCliente==idCli).group_by(conexao.t_docRef).all()
            lista = [n.as_dict() for n in docs]
            return jsonify(lista)
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return jsonify("Error")
    
#Rota para verificar se o documento de referencia já existe na tabela    
@app.route("/docRecfTitulo", methods=["GET", "POST"])
def docRecfTitulo():
    ###################################################################################################
    # API que consulta o documento de referência digitado na tela de cadastro de título, e verifica se
    # na filial que está logado o existe esse documento.
    
    # PARAMETROS:
    #  doc["doc"] = Número do documento que foi passado;
    #  doc["filial"] = Filial que está logado.
    
    # RETORNOS:
    #   return jsonify(False) = Retorna Json com False não esiste;
    #   return jsonify(True) = Retorna Json com True existe;
    #   return jsonify("Error") = Retorna Json caso ocorra um erro.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            if request.method == "POST":
                doc = request.get_json()
                conexao = Gf3004 #Conexão com a tabela de título
                #Query que verifica se o documento de referência já existe na filial logada
                docRef = conexao.query.filter(conexao.t_docRef==doc["doc"], conexao.t_ativo==1, conexao.t_filialOri==doc["filial"]).first()
                if docRef:
                    return jsonify(False)
                else:
                    return jsonify(True)
            
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro)
        return jsonify("Error")
    
#Rota para preencher a lista de titulos
@app.route("/titulos", methods=["GET", "POST"])
def titulos():
    ###################################################################################################
    # API que consulta os títulos para a listagem.
    
    # PARAMETROS:
    #  doc["doc"] = Número do documento que foi passado;
    #  doc["filial"] = Filial que está logado.
    
    # RETORNOS:
    #   return jsonify(lista) = Retorna Json com a lista de títulos;
    #   return jsonify("Error") = Retorna Json caso ocorra um erro.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            if request.method == "POST":
                conexao = Gf3004 #Conexão com a tabela de títulos
                conexao2 = Gf3001 #Conexão com a tabela de clientes 
                conexao3 = Gf3002 #Conexão com a tabela de vendedores
                conexao4 = Gf3003 #Conexão com a tabela de segmentos
                
                dataAtual = datetime.now()
                dataAtual = dataAtual - relativedelta(years=leAnoTitulo())
                dataAtual = dataAtual.strftime("%Y")
                
                #Query que trás todos os títulos exeto os excluidos
                titulos = db.session.query(conexao.t_dataLanc, conexao.t_idCliente, conexao.t_idVendedor,conexao.t_numDoc, func.count(conexao.t_numParcela).label('parcelas'), func.sum(conexao.t_valor).label('total'), conexao2.c_razaosocial.label('cliente'), conexao.t_docRef, conexao4.s_abrev) \
                .filter(conexao.t_ativo == 1, conexao.t_filial == session["filial"], conexao.t_dataLanc >= dataAtual) \
                .join(conexao4, conexao4.s_id == conexao.t_segmento) \
                .join(conexao2, conexao.t_idCliente==conexao2.c_id) \
                .group_by(conexao.t_dataLanc, conexao.t_idCliente, conexao2.c_razaosocial, conexao.t_idVendedor, conexao.t_numDoc, conexao4.s_abrev).order_by(conexao.t_dataLanc)
                lista = []
                for x in titulos:
                    lista.append({"ref": x.t_docRef, "doc": x.t_numDoc, "par": x.parcelas, "cli": filtroNome(x.cliente), "abrev": x.s_abrev, "lanc": filtroData(x.t_dataLanc), "total":filtroValor(x.total)})
                
                return jsonify(lista)
            
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro)
        return jsonify("Error")
    
#Rota para api para utilizar no gráfico    
@app.route("/api-titulos-recebidos", methods=["GET", "POST"])
def titulosRecebidos():
    ###################################################################################################
    # API que consulta os títulos recebidos dos últimos 5 meses.
    
    # PARAMETROS:
    #  Não tem parametros.
    
    # RETORNOS:
    #   return jsonify({"valores": listaValor[::-1], "meses": listaMeses[::-1]}) = Retorna Json com 
    #     a lista de valores e os meses referentes;
    #   return jsonify("Error") = Retorna Json caso ocorra um erro.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            if request.method == "POST":
                conexao = Gf3004 #Conexão com a tabela títulos
                listaValor = []
                listaMeses = []
                for x in range(0, 5):
                    dataAtual = date.today()
                    dataAtual = dataAtual - relativedelta(months=x+1)  
                    nomeMes = dataAtual.strftime("%b %y")
                    ultimoDia = dataAtual.replace(day=monthrange(dataAtual.year, dataAtual.month)[1]).strftime("%Y%m%d")
                    dataAtual = dataAtual.strftime("%Y%m%d")
                    primeiroDia = f"{dataAtual[0:6]}01"
                    
                    #Query que trás todas as baixas dentro do range
                    baixas = db.session.query(func.sum(conexao.t_valor)) \
                    .filter(conexao.t_status==0, conexao.t_dataVenc>=primeiroDia, conexao.t_dataVenc<=ultimoDia) \
                    .order_by(conexao.t_dataVenc).first()
                    
                    listaValor.append(filtroFloat(baixas[0]))
                    listaMeses.append(nomeMes)

                return jsonify({"valores": listaValor[::-1], "meses": listaMeses[::-1]})
            
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return jsonify("Error")
    
#Rota para api para utilizar no gráfico    
@app.route("/api-titulos-receber", methods=["GET", "POST"])
def titulosReceber():
    ###################################################################################################
    # API que consulta os títulos a receber dos próximos 5 meses.
    
    # PARAMETROS:
    #  Não tem parametros.
    
    # RETORNOS:
    #  return jsonify({"valores": listaValor, "meses": listaMeses}) = Retorna Json com 
    #     a lista de valores e os meses referentes;
    #   return jsonify("Error") = Retorna Json caso ocorra um erro.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            if request.method == "POST":
                conexao = Gf3004 #Conexão com a tabela de título
                listaValor = []
                listaMeses = []
                for x in range(0, 5):
                    dataAtual = date.today()
                    dataAtual = dataAtual + relativedelta(months=x+1)
                    nomeMes = dataAtual.strftime("%b %y")
                    ultimoDia = dataAtual.replace(day=monthrange(dataAtual.year, dataAtual.month)[1]).strftime("%Y%m%d")
                    dataAtual = dataAtual.strftime("%Y%m%d")
                    primeiroDia = f"{dataAtual[0:6]}01"
                    
                    #Query que trás todas as futuras baixas dentro do range
                    receber = db.session.query(func.sum(conexao.t_saldo)) \
                    .filter(conexao.t_status==1, conexao.t_dataVenc>=primeiroDia, conexao.t_dataVenc<=ultimoDia) \
                    .order_by(conexao.t_dataVenc).first()
                    
                    listaValor.append(filtroFloat(receber[0]))
                    listaMeses.append(nomeMes)

                return jsonify({"valores": listaValor, "meses": listaMeses})
            
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return jsonify("Error")
    
#Rota para api para utilizar no gráfico    
@app.route("/api-titulos-comparar", methods=["GET", "POST"])
def titulosComparar():
    ###################################################################################################
    # API que consulta a comparação de valores recebidos dos 12 meses entre dois anos.
    
    # PARAMETROS:
    #  Não tem parametros.
    
    # RETORNOS:
    #  return jsonify({"valorresAtual": listaValorAtual, "anoAtual": anoAtual[:4], "valoresAnteriror": listaValorAnterior, 
    #  "anoAnterior": anoAnterior[:4], "meses": listaMeses}) = Retorna Json com a lista de valores e os meses referentes;
    #   return jsonify("Error") = Retorna Json caso ocorra um erro.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            if request.method == "POST":
                conexao = Gf3004 #Conexão com a tabela de título
                listaValorAtual = []
                listaValorAnterior = []
                listaMeses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
                
                for x, i in enumerate(listaMeses):
                    dataAtual = date.today()
                    anoAtual = dataAtual.strftime("%Y%m%d")
                    anoAtual = f"{anoAtual[:4]}0101"
                    
                    anoAtual = datetime.strptime(anoAtual, "%Y%m%d")
                    anoAtual = anoAtual + relativedelta(months=x)
                    ultimoDiaAtual = anoAtual.replace(day=monthrange(anoAtual.year, anoAtual.month)[1]).strftime("%Y%m%d")
                    anoAtual = anoAtual.strftime("%Y%m%d")
                    primeiroDiaAtual = f"{anoAtual[0:6]}01"
                    
                    #Query que consulta o valor recebido nos mêses do ano atual
                    receberAtual = db.session.query(func.sum(conexao.t_valor)) \
                    .filter(conexao.t_status==0, conexao.t_dataVenc>=primeiroDiaAtual, conexao.t_dataVenc<=ultimoDiaAtual) \
                    .order_by(conexao.t_dataVenc).first()
                    
                    listaValorAtual.append(filtroFloat(receberAtual[0]))
                    
                    #Ano anterior
                    anoAnterior = dataAtual - relativedelta(years=1)
                    anoAnterior = anoAnterior.strftime("%Y%m%d")
                    anoAnterior = f"{anoAnterior[:4]}0101"
                    
                    anoAnterior = datetime.strptime(anoAnterior, "%Y%m%d")
                    anoAnterior = anoAnterior + relativedelta(months=x)
                    ultimoDiaAnterior = anoAnterior.replace(day=monthrange(anoAnterior.year, anoAnterior.month)[1]).strftime("%Y%m%d")
                    anoAnterior = anoAnterior.strftime("%Y%m%d")
                    primeiroDiaAnterior = f"{anoAnterior[0:6]}01"
                    
                    #Query que consulta o valor recebido nos mêses do ano anterior
                    receberAnterior = db.session.query(func.sum(conexao.t_valor)) \
                    .filter(conexao.t_status==0, conexao.t_dataVenc>=primeiroDiaAnterior, conexao.t_dataVenc<=ultimoDiaAnterior) \
                    .order_by(conexao.t_dataVenc).first()
                    
                    listaValorAnterior.append(filtroFloat(receberAnterior[0]))

                return jsonify({"valorresAtual": listaValorAtual, "anoAtual": anoAtual[:4], "valoresAnteriror": listaValorAnterior, "anoAnterior": anoAnterior[:4], "meses": listaMeses})
            
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return jsonify("Error")
     
#Rota para api para utilizar no gráfico    
@app.route("/api-tipo-decolucao", methods=["GET", "POST"])
def tipoDevolucao():
    ###################################################################################################
    # API que consulta a comparação dos tipos de devolução dentro do mês atual.
    
    # PARAMETROS:
    #  Não tem parametros.
    
    # RETORNOS:
    #  return jsonify({"biaxas": baixas[0], "baixasDev": baixasDev[0]}) = Retorna Json com o valor de 
    #    devolução e baixa normal dentro do mês;
    #   return jsonify("Error") = Retorna Json caso ocorra um erro.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            if request.method == "POST":
                conexao = Gf3006 #Conexão com a tabela de movimento
                dataAtual = date.today()
                ultimoDia = dataAtual.replace(day=monthrange(dataAtual.year, dataAtual.month)[1]).strftime("%Y%m%d")
                dataAtual = dataAtual.strftime("%Y%m%d")
                primeiroDia = f"{dataAtual[0:6]}01"
                #Query que trás o valor somado no mês atual de baixas normais
                baixas = db.session.query(func.sum(conexao.m_valor)) \
                .filter(conexao.m_ativo==1, or_(conexao.m_idDev=="", conexao.m_idDev==None), conexao.m_dataBaixa>=primeiroDia, conexao.m_dataBaixa<=ultimoDia).first()
                #Query que trás o valor somado no mês atual de baixas por devolução
                baixasDev = db.session.query(func.sum(conexao.m_valor)) \
                .filter(conexao.m_ativo==1, conexao.m_idDev!="", conexao.m_dataBaixa>=primeiroDia, conexao.m_dataBaixa<=ultimoDia).first()
                return jsonify({"biaxas": baixas[0], "baixasDev": baixasDev[0]})
            
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return jsonify("Error")
    
#Api para verificar se o campo documento referência no cadastro de devolução está correto
@app.route("/api-docRef", methods=["GET", "POST"])
def docRef():
    ###################################################################################################
    # API que consulta o documento de referência digitado na tela de cadastro de devolução, e verifica
    # se documento de referência existe.
    
    # PARAMETROS:
    #  data["docRef"] = Número do documento de referência que foi passado;
    #  data["id"] = Id do cliente que foi passado.
    
    # RETORNOS:
    #   return jsonify({"resp": True}) = Retorna Json com True existe;
    #   return jsonify({"resp": False}) = Retorna Json com False não existe;
    #   return jsonify("Error") = Retorna Json caso ocorra um erro.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            if request.method == "POST":
                data = request.get_json()
                conexao = Gf3004 #Conexão com a tabela de título
                #Query que verifica se o documento de referência que foi passado existe para o cliente passado
                docRef = conexao.query.filter(conexao.t_docRef==data["docRef"], conexao.t_idCliente==data["id"]).first()
                if docRef:
                    return jsonify({"resp": True})
                else:
                    return jsonify({"resp": False})
            
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return jsonify("Error")