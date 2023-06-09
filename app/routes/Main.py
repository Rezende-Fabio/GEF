from flask import render_template, request, redirect, flash, session, jsonify
from sqlalchemy import func
from app import app
from ..bd.models import *
from ..extensions.EnviarEmail import EnviaEmail
import random
from werkzeug.security import generate_password_hash
from datetime import datetime
from ..extensions.logs import Logger
import sys
from ..extensions.veriaveis import *


###################################
# Rotas relacionadas ao Index
###################################


#Rota inicial
@app.route("/")
@app.route("/index")
def index():
    ###################################################################################################
    # Função que verifica se máquina que solicitou acesso pode acessar o sistema e rediciona
    # para o index.
    
    # PARAMETROS:
    #   request.remote_addr = IP da máquina que solicitou acesso no sistema.
    
    # RETORNOS:
    #   return render_template("alert.html") = Caso a máquina não tem direito redireciona 
    #     para uma tela de erro;
    #   return f"{BASEDIR}/app/" = Caso a máquina tenha direito redireciona para o index.
    ###################################################################################################
    
    #Verificação dos ips que tem acesso ao sistema
    # with open(f"{get_path_variaveis()}Ips.txt", "r+") as txt:
    #     ips = txt.read()
    
    # if request.remote_addr not in ips:
    #     return render_template("alert.html")
    # else:
    return render_template("index.html")
    

#Rota para autenticação no sistema
@app.route("/autenticar", methods=["POST"])
def autenticar():
    ###################################################################################################
    # Função que verifica se o usário existe no banco e faz a autenticação do mesmo no sistema.
    
    # PARAMETROS:
    #   request.form["usuario"] = Usuário que foi digitado no input da tela login;
    #   request.form["senha"] = Senha que foi digitada no input da tela login.
    
    # RETORNOS:
    #   return render_template("menu.html", contexto=contexto) = Redireciona para o menu do 
    #     sistema pasando contexto com as veriáveis para utilizar no template;
    #   return redirect("/") = Redireciona para o index.
    ###################################################################################################
    
    if request.method == "POST":
        user = request.form["usuario"].upper()
        pssd = request.form["senha"].upper() 
        filial = int(request.form["filial"])
        conexao = SysUsers #Conexão com a tabela de usuários
        usuarios = conexao.query.filter_by(s_ativo=1) #Query trazendo apenas o usuários ativos
        for usuario in usuarios:
            if usuario.s_usuario == user and usuario.verificaSenha(pssd): #Chama função de verificação da senha com hash
                session.permanent = True
                session["usuario_logado"] = user #Variável do cookie que guarda o nome do usuário logado
                session["user_admin"] = usuario.s_admin #Variável do cookie que guarda se o usuário é admin ou não
                session["filial"] = filial #Variável do cookie que guarda a filial que o usuário escolheu
                
                usuario = usuario
                
                conexao = Gf3004 #Conexão com a tabela de títulos
                conexao2 = Gf3003 #Conexão com a tabela de segmentos
                #Query para mostar os ultimos 5 títulos cadastrados
                titulos = db.session.query(conexao.t_dataLanc, conexao.t_idCliente, conexao.t_idVendedor, conexao.t_numDoc, func.count(conexao.t_numParcela).label('parcelas'), conexao.t_docRef, conexao2.s_abrev).filter(conexao.t_ativo == 1, conexao.t_filial == session["filial"]).join(conexao2, conexao2.s_id == conexao.t_segmento).group_by(conexao.t_dataLanc, conexao.t_idCliente, conexao.t_idVendedor, conexao.t_numDoc, conexao2.s_abrev).order_by(conexao.t_numDoc.desc())
                paginasTi = titulos.paginate(page=1, per_page=5)
                
                conexao3 = Gf3006 #Conexão com a tabela de movimento
                #Query para mostar as ultimas 5 baixas cadastradas
                baixas = db.session.query(conexao3.m_docRef, conexao3.m_numDoc, conexao3.m_parcela, conexao3.m_idCliente, conexao3.m_dataBaixa, conexao3.m_valor, conexao3.m_tipoBaixa).filter(conexao3.m_ativo == 1, conexao3.m_filial == session["filial"]).order_by(conexao3.m_id.desc())
                paginasBa = baixas.paginate(page=1, per_page=5)
                
                conexao4 = Gf3002
                vendedores = conexao4.query.count()
                
                conexao5 = Gf3001
                clientes = conexao5.query.count()
                
                qtdeTitulos = conexao.query.filter(conexao.t_ativo==1).count()
                
                contexto = {"paginasTi": paginasTi, "paginasBa": paginasBa, "qtdeClientes": clientes, "qtdeVendedores": vendedores, "qtdeTitulo": qtdeTitulos, "usuario": usuario} #Dicionário contendo as variáveis para utilizar no template
                 
                return render_template("menu.html", contexto=contexto)
            
        else:
            flash("Usuário/Senha incorreto!") #retorna mesnagem caso usuário ou senha entejam incorretos
            return redirect("/")

#Rota para fazer logout
@app.route("/logout")
def logout():
    ###################################################################################################
    # Função que zera as variáveis do cookie e faz o logout no sistema.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return redirect("/") = Redireciona para o index.
    ###################################################################################################
    
    session["usuario_logado"] = False
    session["filial"] = False
    session["user_admin"] = False
    
    return redirect("/")

#Rota para Tela inincial
@app.route("/base")
def base():
    ###################################################################################################
    # Função que pesquisa os ultimos 5 títulos e baixas, renderiza o menu.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return render_template("menu.html", contexto=contexto) = Redireciona para o menu do 
    #     sistema pasando contexto com as veriáveis para utilizar no template;
    #   return redirect("/") = Redireciona para o index;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    try:
        if session["usuario_logado"]:
            conexao = Gf3004 #Conexão com a tabela de títulos
            conexao2 = Gf3003 #Conexão com a tabela de segmentos
            #Query para mostar os ultimos 5 títulos cadastrados
            titulos = db.session.query(conexao.t_dataLanc, conexao.t_idCliente, conexao.t_idVendedor, conexao.t_numDoc, func.count(conexao.t_numParcela).label('parcelas'), conexao.t_docRef, conexao2.s_abrev).filter(conexao.t_ativo == 1, conexao.t_filial == session["filial"]).join(conexao2, conexao2.s_id == conexao.t_segmento).group_by(conexao.t_dataLanc, conexao.t_idCliente, conexao.t_idVendedor, conexao.t_numDoc, conexao2.s_abrev).order_by(conexao.t_numDoc.desc())
            paginasTi = titulos.paginate(page=1, per_page=5)
            
            conexao3 = Gf3006 #Conexão com a tabela de movimentos
            #Query para mostar as ultimas 5 baixas cadastradas
            baixas = db.session.query(conexao3.m_docRef, conexao3.m_numDoc, conexao3.m_parcela, conexao3.m_idCliente, conexao3.m_dataBaixa, conexao3.m_valor, conexao3.m_tipoBaixa).filter(conexao3.m_ativo == 1, conexao3.m_filial == session["filial"]).order_by(conexao3.m_id.desc())
            paginasBa = baixas.paginate(page=1, per_page=5)
            
            conexao4 = Gf3002 #Conexão com a tabela de vendedores
            #Query que trás a quantidade de vendedores cadastrados no sistema
            vendedores = conexao4.query.count()
            
            conexao5 = Gf3001 #Conexão com a tabela de clientes
            #Query que trás a quantidade de clientes cadastrados no sistema
            clientes = conexao5.query.count()
            
            #Query que trás a quantidade de títulos cadastrados no sistema
            qtdeTitulos = conexao.query.filter(conexao.t_ativo==1).count() 
            
            contexto = {"paginasTi": paginasTi, "paginasBa": paginasBa, "qtdeClientes": clientes, "qtdeVendedores": vendedores, "qtdeTitulo": qtdeTitulos} #Dicionário contendo as variáveis para utilizar no template
            
            return render_template("menu.html", contexto=contexto) #Retorna passando a lista das ultimos 5 títulos e baixas
        else:
            return redirect("/")
    
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")
  
#Rota para esqueci a senha 
@app.route("/esqueci-senha", methods=["GET", "POST"])
def esqueciSenha():
    ###################################################################################################
    #   Função que procura no banco de dados usuário correspondente ao usuário e e-mail digitado.
    #   Se existir ele gera uma senha temporária e envia no e-mail, e muda o campo s_novaSenha 
    # para 1 (ao logar no sistema esse campo estiver 1, será exibida uma tela para alterção
    # de senha).
    #   Se não existir ele retorna um aviso para o usuário.
    
    # PARAMETROS:
    #   request.form["email"] = E-mail digitado no input do modal;
    #   request.form["usuario"] = Usuário digitado no input do modal.
    
    # RETORNOS:
    #   return jsonify({"success": True}) = Retorna Json True quando o e-mail é enviado com sucesso;
    #   return jsonify({"success": False, "email": "Error"}) = Retorna Json Flase e Error quando
    #     não é possivel enviar o e-mail;
    #   return jsonify({"success": False}) = Retorna Json quando o usuário e o e-mail não existem 
    #     no banco;
    #   return render_template("index.html", contexto=contexto) = Redireciona para o index do 
    #     sistema pasando contexto com as veriáveis para utilizar no template.
    ###################################################################################################
    
    if request.method == "POST":
        email = request.form["email"] 
        user = request.form["usuario"].upper()
        conexao = SysUsers #Conexão com a tabela de usuário
        usuario = conexao.query.filter_by(s_usuario=f"{user}", s_email=f"{email}").first() #Query trazendo o usuário correspondente ao usuário e e-mail
        if usuario:
            senha = []
            for x in range(0,5): #Gera senha com 5 números aleatórios
                senha.append(random.randint(0, 9))
                
            senha = "".join(map(str, senha)) #Transforma a lista em string
            usuario.s_senha = generate_password_hash(senha) #Gera hash da senha temporária e grava no banco
            usuario.s_novaSenha = 1 #Grava 1 no banco, para mostrar modal de mudaça de senha no proximo login
            db.session.commit()
            
            respEmail = EnviaEmail.enviarEmail(email, senha) #Função para enviar e-mail com a senha temporária
            
            if respEmail: #Verifica o retorno da função enviar e-mail
                return jsonify({"success": True})
            else:
                return jsonify({"success": False, "email": "Error"})
            
        else:
            return jsonify({"success": False})
    
    contexto = {"aviso": 1} #Dicionário contendo as variáveis utilizadas no template 
    return render_template("index.html", contexto=contexto) #Retorna passando aviso = 1 para mostral modal no template
        
#Rota para a atualização da senha ao entrar no sistema
@app.route("/cad-senha/<id>", methods=["GET", "POST"])
def cadastraNovaSenha(id):
    ###################################################################################################
    # Função que recebe a nova senha do usuário e garva no banco.
    
    # PARAMETROS:
    #   id = Id do usuario que solicitou a troca da senha.
    
    # RETORNOS:
    #   return redirect("/base") = Redireciona para o menu do sistema;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            if request.method == "POST":
                conexao = SysUsers #Conexão com a tabela de usuário
                usuario = conexao.query.get(id) #Query trazendo o usuário de acordo com o id passado
                usuario.s_senha = generate_password_hash(request.form["senha"].upper()) #Gera o hash para gravar a nova senha no banco 
                usuario.s_novaSenha = 0 #Muda o status para zero novamente
                db.session.commit()
                return redirect("/base")
        else:
            return redirect("/")
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index") 
    
#Rota para exibir modal de confrimação para troca de filial    
@app.route("/troca-filial")
def trocaFilial():
    ###################################################################################################
    # Função que mostra modal para confrimação para a troca de filial.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   render_template("menu.html", contexto=contexto) = Redireciona para o menu do sistema
    #     passando o contexto contendo a variáveis para utilizar no template;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            conexao = Gf3004 #Conexão com a tabela de títulos
            conexao2 = Gf3003 #Conexão com a tabela de segmentos
            #Query para mostrar os ultimos 5 títulos cadatrados
            titulos = db.session.query(conexao.t_dataLanc, conexao.t_idCliente, conexao.t_idVendedor, conexao.t_numDoc, func.count(conexao.t_numParcela).label('parcelas'), conexao.t_docRef, conexao2.s_abrev).filter(conexao.t_ativo == 1, conexao.t_filial == session["filial"]).join(conexao2, conexao2.s_id == conexao.t_segmento).group_by(conexao.t_dataLanc, conexao.t_idCliente, conexao.t_idVendedor, conexao.t_numDoc, conexao2.s_abrev).order_by(conexao.t_numDoc.desc())
            paginasTi = titulos.paginate(page=1, per_page=5)
            
            conexao3 = Gf3006
            #Query para mostrar os ultimas 5 baixas cadatradas
            baixas = db.session.query(conexao3.m_docRef, conexao3.m_numDoc, conexao3.m_parcela, conexao3.m_idCliente, conexao3.m_dataBaixa, conexao3.m_valor, conexao3.m_tipoBaixa).filter(conexao3.m_ativo == 1, conexao3.m_filial == session["filial"]).order_by(conexao3.m_id.desc())
            paginasBa = baixas.paginate(page=1, per_page=5)
            
            contexto = {"aviso": 2, "paginasTi": paginasTi, "paginasBa": paginasBa} #Dicionário contendo as variáveis para utilizar no template
             
            return render_template("menu.html", contexto=contexto)
        else:
            return redirect("/")
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")
    
#Rota para troca de filial
@app.route("/filial")
def filial():
    ###################################################################################################
    # Função que efetua a troca de filia.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   render_template("menu.html", contexto=contexto) = Redireciona para o menu do sistema
    #     passando o contexto contendo a variáveis para utilizar no template;
    #   return redirect("/") = Redireciona para o index se o usuário não estiver logado;
    #   return redirect("/index") = Redireciona para o index quando ocorre uma exeção.
    ###################################################################################################
    
    try:
        if session["usuario_logado"]:
            if session["filial"] == 1: #Troca a Filial na sessão do cookie
                session["filial"] = 2
            else: 
                session["filial"] = 1
                
            conexao = Gf3004 #Conexão com a tabela de títulos
            conexao2 = Gf3003 #Conexão com a tabela de segmentos
            #Query para mostrar os ultimos 5 títulos cadatrados
            titulos = db.session.query(conexao.t_dataLanc, conexao.t_idCliente, conexao.t_idVendedor, conexao.t_numDoc, func.count(conexao.t_numParcela).label('parcelas'), conexao.t_docRef, conexao2.s_abrev).filter(conexao.t_ativo == 1, conexao.t_filial == session["filial"]).join(conexao2, conexao2.s_id == conexao.t_segmento).group_by(conexao.t_dataLanc, conexao.t_idCliente, conexao.t_idVendedor, conexao.t_numDoc, conexao2.s_abrev).order_by(conexao.t_numDoc.desc())
            paginasTi = titulos.paginate(page=1, per_page=5)
            
            conexao3 = Gf3006 #Conexão com a tabela de movimento
            #Query para mostrar os ultimas 5 baixas cadatradas
            baixas = db.session.query(conexao3.m_docRef, conexao3.m_numDoc, conexao3.m_parcela, conexao3.m_idCliente, conexao3.m_dataBaixa, conexao3.m_valor, conexao3.m_tipoBaixa).filter(conexao3.m_ativo == 1, conexao3.m_filial == session["filial"]).order_by(conexao3.m_id.desc())
            paginasBa = baixas.paginate(page=1, per_page=5)
            
            conexao4 = Gf3002 #Conexão com a tabela de vendedores
            #Query que trás a quantidade de vendedores cadastrados no sistema
            vendedores = conexao4.query.count()
            
            conexao5 = Gf3001 #Conexão com a tabela de clientes
            #Query que trás a quantidade de clientes cadastrados no sistema
            clientes = conexao5.query.count()
            
            #Query que trás a quantidade de títulos cadastrados no sistema
            qtdeTitulos = conexao.query.filter(conexao.t_ativo==1).count() 
            
            contexto = {"paginasTi": paginasTi, "paginasBa": paginasBa, "qtdeClientes": clientes, "qtdeVendedores": vendedores, "qtdeTitulo": qtdeTitulos} #Dicionário contendo as variáveis para utilizar no template
            
            return render_template("menu.html", contexto=contexto)
        else:
            return redirect("/")
        
    except Exception as erro:
        Logger.logErro(sys.exc_info()[0], request.url, erro) #Gera um log de erro passando a URL e o erro
        return redirect("/index")