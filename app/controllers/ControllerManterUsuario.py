from ..models.dao.ManterUsuarioDao import ManterUsuarioDao
from ..models.entity.Usuario import Usuario

class ControllerManterUsuario:
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

        if form["useradmin"] == "1": userAdmin = True
        else: userAdmin = False

        usuario = Usuario(nome=form["nome"].upper(), usuario=form["usuario"].upper(), email=form["email"], admin=userAdmin, hashSenhaNova="", senhaNova=False, ativo=True)
        usuario.gerarSenha(form["senha"].upper())

        manterUsuarioDao = ManterUsuarioDao()

        if manterUsuarioDao.inserirUsuario(usuario):
            return True
        else:
            return False
        

    def editarUsuario(self, form: dict, idUser: int) -> bool:
        """
        Essa função recebe um dicionário contendo as informações de um usuário específico para atualizar.

        :param form: Um dicionário com os dados do usuário a ser inserido.

        :return: True se a inserção for bem-sucedida, False caso contrário.
        """

        if form["useradmin"] == "1": userAdmin = True
        else: userAdmin = False

        manterUsuarioDao = ManterUsuarioDao()

        usuario = Usuario(id=idUser, nome=form["nome"].upper(), usuario=form["usuario"].upper(), senha=form["senha"], email=form["email"], admin=userAdmin)
        
        if usuario.senha != manterUsuarioDao.consultarSenhaAntiga(idUser):
            usuario.gerarSenha(form["senha"].upper())
        
        if manterUsuarioDao.editarUsuario(usuario):
            return True
        else:
            return False
