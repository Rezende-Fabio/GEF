from ..Tables import SysUsers

class LoginDao:
    """
    Classe Dao para o login do sistema
    @tables - SysUsers
    @author - Fabio
    @version - 1.0
    @since - 29/09/2023
    """

    def consultarUsuario(self, usuario: str) -> SysUsers:
        user = SysUsers.query.filter(SysUsers.s_usuario==usuario).first()

        return user