from ...configurations.DataBase import DB
from ...extensions.logs import Logger
from ..entity.Usuario import Usuario
from ..Tables import SysUsers
import sys


class ManterUsuarioDao:
    """
    Classe Dao para o CRUD dos usuários do sistema
    @tables - SysUsers
    @author - Fabio
    @version - 1.0
    @since - 29/09/2023
    """

    def inserirUsuario(self, usuario: Usuario) -> bool:
        user = SysUsers(s_usuario=usuario.usuario, 
                                    s_senha=usuario.senha, 
                                    s_nome=usuario.nome, 
                                    s_email=usuario.email, 
                                    s_admin=usuario.admin, 
                                    s_ativo=usuario.ativo, 
                                    s_novaSenha=usuario.senhaNova,
                                    s_complex=usuario.complex)
        try:
            DB.session.add(user)
            DB.session.commit()

            return True
        except Exception as erro:
            print(erro)
            return False
        
    def editarUsuario(self, usuario: Usuario) -> bool:
        #Campos atualizar
        campos = {
            "s_usuario": usuario.usuario,
            "s_senha": usuario.senha,
            "s_nome": usuario.nome,
            "s_email": usuario.email,
            "s_admin": usuario.admin
        }

        try:
            SysUsers.query.filter(SysUsers.id==usuario.id).update(campos)
            DB.session.commit()

            return True
        except Exception as erro:
            print(erro)
            return False
        

    def consultarSenhaAntiga(self, idUser: int) -> str:
        usuario = SysUsers.query.filter(SysUsers.id==idUser).first()

        return usuario.s_senha
    