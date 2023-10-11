from flask_login import login_user, logout_user
from ..models.entity.Usuario import Usuario
from ..models.dao.LoginDao import LoginDao
from flask import session

class ControllerLogin:
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

        loginDao = LoginDao()
        usersResp = loginDao.consultarUsuario(usuario=form["usuario"].upper())

        if usersResp:
            user = Usuario(id=usersResp.id, usuario=usersResp.s_usuario, senha=form["senha"].upper(), complex=usersResp.s_complex, 
                           senhaCompara=usersResp.s_senha, ativo=usersResp.s_ativo, admin=usersResp.s_admin, nome=usersResp.s_nome,
                           senhaNova=usersResp.s_novaSenha)
            if user.ativo:
                if user.verificarSenha():
                    session["usuario"] = user.toJson()
                    session["filial"] = int(form["filial"])
                    return 1
                else:
                    return 2
            else:
                return 3
        else:
            return 4




