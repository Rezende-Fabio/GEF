from ..configurations.DataBase import DB
from ..response.Response import Response
from ..models.Models import SysUsers
from ..extensions.logs import Logger
from flask import session

class ControllerManterUsuario(Response):
    """
    Classe Controller para as funções relacionadas ao CRUD dos usuários
    @author - Fabio
    @version - 1.0
    @since - 29/09/2023
    """

    def inserirUsuario(self, form: dict) -> bool:
        """
        Essa função recebe um dicionário contendo as informações do usuário para a insersão no sistema.

        :param form: Um dicionário com os dados do usuário a ser inserido.

        :return: True se a inserção for bem-sucedida, False caso contrário.
        """

        try:
            if form["useradmin"] == "1": userAdmin = True
            else: userAdmin = False

            usuario = SysUsers(s_nome=form["nome"].upper(), s_usuario=form["usuario"].upper(), s_email=form["email"], s_admin=userAdmin, s_novaSenha=False, s_ativo=True)
            usuario.gerarSenha(form["senha"].upper())

            DB.session.add(usuario)
            DB.session.commit()

            Logger.log("Inserção de Usuário", session["usuario"], session["filial"], f"Nome: {form['nome']}")

            return self.redirect('usuarioBlue.listaUsuarios', mensagem=f"Usuário {form['usuario'].upper()} incluido com sucesso!", categoria="success")
        except Exception as erro:
            print(erro)
            return False
        

    def editarUsuario(self, form: dict, idUser: int) -> bool:
        """
        Essa função recebe um dicionário contendo as informações de um usuário específico para atualizar.

        :param form: Um dicionário com os dados do usuário a ser inserido.

        :return: True se a inserção for bem-sucedida, False caso contrário.
        """

        try:

            if form["useradmin"] == "1": userAdmin = True
            else: userAdmin = False

            userSenhaAntiga = SysUsers.query.get(idUser)

            usuario = SysUsers(s_nome=form["nome"].upper(), s_usuario=form["usuario"].upper(), s_senha=form["senha"], 
                               s_complex=userSenhaAntiga.s_complex, s_email=form["email"], s_admin=userAdmin)

            if usuario.s_senha != userSenhaAntiga.s_senha:
                usuario.gerarSenha(form["senha"].upper())

            SysUsers.query.filter(SysUsers.id==idUser).update(usuario.items())
            DB.session.commit()

            Logger.log("Alteração de Usuário", session["usuario"], session["filial"], f"ID: {id}")

            return self.redirect('usuarioBlue.listaUsuarios', mensagem=f"Usuário {form['usuario'].upper()} atualizado com sucesso!", categoria="success")
        except Exception as erro:
            print(erro)
            return False
