from flask_login import login_user, logout_user, login_required
from ..httpResponse.HttpResponse import HttpResponse
from flask import session, request, abort, g
from ..models.Models import SysUsers
from ..extensions.Log import Log
import traceback
import sys


class ControllerLogin(HttpResponse, Log):
    """
    Classe Controller para as funções relacionadas ao login do sistema
    @author - Fabio
    @tables - SysUsers
    @version - 1.0
    @since - 29/09/2023
    """

    def efetuarLogin(self) -> HttpResponse:
        try:
            form = request.form
            usersResp = SysUsers.query.filter(SysUsers.s_usuario==form["usuario"].upper()).first()

            if usersResp:
                if usersResp.s_ativo:
                    if usersResp.verificarSenha(form["senha"].upper()):
                        login_user(usersResp)
                        session["usuario"] = usersResp.toJson()
                        session["filial"] = int(form["filial"])
                        session.permanent = True

                        return self.responseRedirect(url="dashboardBlue.dashboard")
                    else:
                        return self.responseRedirect(url="indexBlue.index", mensagem="Usuário/Senha incorreto!", categoria="danger")
                else:
                    return self.responseRedirect(url="indexBlue.index", mensagem="Usuário deletado", categoria="danger")
            else:
                return self.responseRedirect(url="indexBlue.index", mensagem="Usuário não existe", categoria="danger")
            
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)


    @login_required
    def efetuarLogout(self) -> HttpResponse:
        try:
            logout_user()
            session.clear()
            g.clear()
            return self.responseRedirect(url="indexBlue.index")
        
        except:
            tipoExcecao, valorExcecao, tb = sys.exc_info()
            tracebackInfo = traceback.extract_tb(tb)
            self.geraLogErro(tipoExcecao, valorExcecao, tracebackInfo, request.url)
            abort(500)
        
