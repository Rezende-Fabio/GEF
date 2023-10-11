from typing import Optional
import bcrypt

class Usuario:
    """
    Classe Usuário
    @author - Fabio
    @version - 1.0
    @since - 29/09/2023
    """
    id: int
    nome: str
    email: str
    usuario: str
    senha: str
    admin: bool
    complex: str
    ativo: bool
    senhaCompara: str
    senhaNova: bool
    hashSenhaNova: str

    def __init__(self, id: Optional[int]=None, nome: Optional[str]=None, email: Optional[str]=None, usuario: Optional[str]=None, 
                 senha: Optional[str]=None, complex: Optional[str]=None, ativo: Optional[bool]=None, senhaCompara: Optional[str]=None, 
                 senhaNova: Optional[bool]=None, hashSenhaNova: Optional[str]=None, admin: Optional[bool]=None) -> None:
        self._id = id
        self._nome = nome
        self._email = email
        self._usuario = usuario
        self._senha = senha
        self._admin = admin
        self._complex = complex
        self._ativo = ativo
        self._senhaCompara = senhaCompara
        self._senhaNova = senhaNova
        self._hashSenhaNova = hashSenhaNova

    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, id: int) -> None:
        self._id = id

    @property
    def nome(self) -> str:
        return self._nome
    
    @nome.setter
    def nome(self, nome: str) -> None:
        self._nome = nome

    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, email: str) -> None:
        self._email = email

    @property
    def grupo(self) -> str:
        return self._grupo
    
    @grupo.setter
    def grupo(self, grupo: str) -> None:
        self._grupo = grupo
    
    @property
    def usuario(self) -> str:
        return self._usuario
    
    @usuario.setter
    def usuario(self, usuario: str) -> None:
        self._usuario = usuario
    
    @property
    def senha(self) -> str:
        return self._senha
    
    @senha.setter
    def senha(self, senha: str) -> None:
        self._senha = senha
  
    @property
    def admin(self) -> bool:
        return self._admin
    
    @admin.setter
    def admin(self, admin: bool) -> None:
        self._admin = admin
    
    @property
    def complex(self) -> str:
        return self._complex
    
    @complex.setter
    def complex(self, complex: str) -> None:
        self._complex = complex
    
    @property
    def ativo(self) -> bool:
        return self._ativo
    
    @ativo.setter
    def ativo(self, ativo: bool) -> None:
        self._ativo = ativo
    
    @property
    def senhaCompara(self) -> str:
        return self._senhaCompara
    
    @senhaCompara.setter
    def senhaCompara(self, senhaCompara: str) -> None:
        self._senhaCompara = senhaCompara
    
    @property
    def senhaNova(self) -> bool:
        return self._senhaNova
    
    @senhaNova.setter
    def senhaNova(self, senhaNova: bool) -> None:
        self._senhaNova = senhaNova
    
    @property
    def hashSenhaNova(self) -> str:
        return self._hashSenhaNova
    
    @hashSenhaNova.setter
    def hashSenhaNova(self, hashSenhaNova: str) -> None:
        self._hashSenhaNova = hashSenhaNova
    

    def gerarSenha(self, senha: str) -> None:
        salt = bcrypt.gensalt(8)
        hash = bcrypt.hashpw(senha.encode('utf-8'), salt)
        self._senha = hash.decode("utf-8")
        self._complex = salt.decode("utf-8")
        

    def verificarSenha(self) -> bool:
        hash = bcrypt.hashpw(self._senha.encode('utf-8'), bytes(self._complex, 'utf-8'))
        if hash.decode('utf-8') == self._senhaCompara:
            return True
        else:
            return False
        
    
    def toJson(self) -> dict:
        json = {
            "id": self._id,
            "nome": self._nome,
            "usuario": self._usuario,
            "admin": self._admin
        }

        return json