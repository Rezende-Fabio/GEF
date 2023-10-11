from flask_login import login_user, logout_user
from ..models.Models import SysUsers
from flask import session
from ..response.Response import Response


class ControllerLogin(Response):
    """
    Classe Controller para as funções relacionadas ao login do sistema
    @author - Fabio
    @version - 1.0
    @since - 29/09/2023
    """

    def efetuarLogin(self, form: dict) -> int:
        """
        Realiza o processo de login do usuário.

        :param user: Um dicionário com o usuário e senha.

        :return: Um código indicando o resultado do processo de login.
            1 - Login bem-sucedido.
            2 - Senha/Usuário estão incorretos.
            3 - Usuário deletado.
            4 - Usuário não encontrado.
        """

        usersResp = SysUsers.query.filter(SysUsers.s_usuario==form["usuario"].upper()).first()

        if usersResp:
            if usersResp.s_ativo:
                if usersResp.verificarSenha(form["senha"].upper()):
                    login_user(usersResp)
                    session["usuario"] = usersResp.toJson()
                    session["filial"] = int(form["filial"])
                    session.permanent = True

                    return self.redirect(url="dashboardBlue.dashboard")
                else:
                    return self.redirect(url="indexBlue.index", mensagem="Usuário/Senha incorreto!")
            else:
                return self.redirect(url="indexBlue.index", mensagem="Usuário deletado")
        else:
            return self.redirect(url="indexBlue.index", mensagem="Usuário não existe")



    def efetuarLogout(self) -> None:
        """
        Realiza o processo de logout do usuário.
        """

        logout_user()
        session.clear()

        return self.redirect(url="mainBlue.index")

        
