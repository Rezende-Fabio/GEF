from ..httpResponse.HttpResponse import HttpResponse
from flask import session, abort, request
from ..configurations.DataBase import DB
from flask_login import login_required
from ..models.Models import SysUsers
from ..extensions.Log import Log
import traceback
import sys

class ControllerUsuario(HttpResponse, Log):
    """
    Classe Controller para as funções relacionadas ao CRUD dos usuários
    @author - Fabio
    @tables - SysUsers
    @version - 1.0
    @since - 17/10/2023
    """

    @login_required
    def renderListaUsuarios(self) -> HttpResponse:
        try:
            context = {"active": "usuario", "titulo": "Lista de Usuários"}
            return self.responseRender(arquivo="usuario/listaUsuarios.html", context=context)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)

    
    @login_required
    def renderCadUsuario(self) -> HttpResponse:
        try:
            context = {"titulo": "Inclusão de Usuário", "botao": "Gravar", "active": "usuario", "editar": False}
            return self.responseRender(arquivo="usuario/cadUsuario.html", context=context)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def renderEditUsuario(self, idUser: int) -> HttpResponse:
        try:
            usuario = SysUsers.query.get(idUser)
            context = {"titulo": "Atualização de Usuário", "botao": "Alterar", "usuario": usuario, "editar": True}
            return self.responseRender(arquivo="usuario/cadUsuario.html", context=context)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def consultarUsuario(self, idUser: int) -> HttpResponse:
        try:
            usuario = SysUsers.query.get(idUser)
            return self.responseJson(body=usuario.toJson(), status=200)
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)
    

    @login_required
    def consultarUsuarios(self) -> HttpResponse:
        try:
            usuarios = DB.session.query(SysUsers.id, SysUsers.s_usuario, SysUsers.s_nome, SysUsers.s_admin).filter(SysUsers.s_ativo!=False)
            listaUsuarios = []
            for user in usuarios:
                dictUser = {
                    "cod": user.id, 
                    "user": user.s_usuario, 
                    "nome": user.s_nome, 
                    "admin": "SIM" if user.s_admin else "NÃO"
                }
                listaUsuarios.append(dictUser)

            return self.responseJson(body=listaUsuarios, status=200)

        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def inserirUsuario(self) -> HttpResponse:
        try:
            form = request.form
            #Verifica se as senhas que foram digitadas são iguais
            if form["senha"].upper().strip() != form["confSenha"].upper().strip():
                return self.responseJson(status=400)

            if form["useradmin"] == "1": userAdmin = True
            else: userAdmin = False

            usuario = SysUsers(s_nome=form["nome"].upper(), s_usuario=form["usuario"].upper(), s_email=form["email"], s_admin=userAdmin, s_novaSenha=False, s_ativo=True)
            usuario.gerarSenha(form["senha"].upper())

            DB.session.add(usuario)
            DB.session.commit()

            self.geraLogDiario("Inseriu um Usuário", session["usuario"]["usuario"], session["filial"], f"Nome: {form['nome']}")
            return self.responseJsonMessage(status=204, mensagem=f"Usuário {form['usuario'].upper()} incluido com sucesso!", categoria="success")
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def editarUsuario(self, idUser: int) -> HttpResponse:
        try:
            form = request.form
            #Verifica se as senhas que foram digitadas são iguais
            if form["senha"].upper().strip() != form["confSenha"].upper().strip():
                return self.responseJson(status=400)

            if form["useradmin"] == "1": userAdmin = True
            else: userAdmin = False

            userSenhaAntiga = SysUsers.query.get(idUser)

            usuario = SysUsers(s_nome=form["nome"].upper(), s_usuario=form["usuario"].upper(), s_senha=form["senha"], 
                               s_complex=userSenhaAntiga.s_complex, s_email=form["email"], s_admin=userAdmin)
            
            #Verifica se a senha continua a mesma
            if usuario.s_senha != userSenhaAntiga.s_senha:
                usuario.gerarSenha(form["senha"].upper())

            SysUsers.query.filter(SysUsers.id==idUser).update(usuario.items())
            DB.session.commit()

            self.geraLogDiario("Alterou um Usuário", session["usuario"]["usuario"], session["filial"], f"ID: {idUser}")
            return self.responseJsonMessage(status=204, mensagem=f"Usuário {form['usuario'].upper()} atualizado com sucesso!", categoria="success")
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)

    
    @login_required
    def excluirUsuario(self, idUser: int) -> HttpResponse:
        try:
            usuario = SysUsers.query.get(idUser)

            if usuario.s_usuario == session["usuario"]["usuario"]:
                return self.responseJsonMessage(status=400, mensagem="Usuário logado não pode ser excluido!", categoria="danger")
            elif idUser == 1:
                return self.responseJsonMessage(status=400, mensagem="O usuário ADMIN não pode ser excluido!", categoria="danger")
            else:
                campos = {
                    "s_ativo": False
                }

                SysUsers.query.filter(SysUsers.id==idUser).update(campos)
                DB.session.commit()

                self.geraLogDiario("Excluiu um Usuário", session["usuario"]["usuario"], session["filial"], f"ID: {idUser}") #Gera log informando que foi feita exclusão do usuário
                return self.responseJsonMessage(status=204, mensagem=f"Usuário {usuario.s_usuario} excluido com sucesso!", categoria="success")
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)
