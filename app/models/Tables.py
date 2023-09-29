from sqlalchemy import Column, String, DateTime, Boolean, Float, Integer, Numeric, ForeignKey
from werkzeug.security import check_password_hash
from ..configurations.DataBase import DB


#Usuários
class SysUsers(DB.Model):
    s_codigo = DB.Column(DB.Integer, primary_key=True)
    s_usuario = DB.Column(DB.String(10))
    s_senha = DB.Column(DB.String(32))
    s_nome = DB.Column(DB.String(80))
    s_email = DB.Column(DB.String(80), unique=True)
    s_admin = DB.Column(DB.Boolean)
    s_ativo = DB.Column(DB.Boolean)
    s_novaSenha = DB.Column(DB.Boolean)
    
    def __repr__(self):
        return f"{self.s_codigo}"
    
    def verificaSenha(self, senha):
        return check_password_hash(self.s_senha, senha)

#Cliente
class Gf3001(DB.Model):
    c_id = DB.Column(DB.String(10), primary_key=True)
    c_codigo = DB.Column(DB.String(9))
    c_loja = DB.Column(DB.String(2))
    c_razaosocial = DB.Column(DB.String(45))
    c_cpfcnpj = DB.Column(DB.String(14))
    c_inscricao = DB.Column(DB.String(18))
    c_email = DB.Column(DB.String(45))
    c_endereco = DB.Column(DB.String(60))
    c_bairro = DB.Column(DB.String(30))
    c_cep = DB.Column(DB.String(9))
    c_cidade = DB.Column(DB.String(40))
    c_uf = DB.Column(DB.String(18))
    c_telefone = DB.Column(DB.String(11))
    c_codvend = DB.Column(DB.String(6))
    c_dataCriacao = DB.Column(DB.String(8))
    c_ativo = DB.Column(DB.Boolean)
    
    def as_dict(self):
        return {"nome": f"{self.c_id} - {self.c_razaosocial}"}

#Vendedor
class Gf3002(DB.Model):
    v_id = DB.Column(DB.String(10), primary_key=True)
    v_nome = DB.Column(DB.String(45))
    v_endereco = DB.Column(DB.String(60))
    v_bairro = DB.Column(DB.String(30))
    v_cidade = DB.Column(DB.String(40))
    v_uf = DB.Column(DB.String(18))
    v_cep = DB.Column(DB.String(9))
    v_contato = DB.Column(DB.String(45))
    v_cpfcnpj = DB.Column(DB.String(14))
    v_inscricao = DB.Column(DB.String(18))
    v_telefone = DB.Column(DB.String(11))
    v_celular = DB.Column(DB.String(11))
    v_comis = DB.Column(DB.Float)
    v_email = DB.Column(DB.String(45))
    v_ativo = DB.Column(DB.Boolean)
    
    def as_dict(self):
        return {"nome": f"{self.v_id} - {self.v_nome}"}

#Seguimentos
class Gf3003(DB.Model):
    s_id = DB.Column(DB.Integer, primary_key=True)
    s_desc = DB.Column(DB.String(40))
    s_abrev = DB.Column(DB.String(5))
    s_filial = DB.Column(DB.Integer)
    
    def __repr__(self):
        return f"{self.s_abrev}"

#Titulo   
class Gf3004(DB.Model):
    t_id = DB.Column(DB.Integer, primary_key=True)
    t_numDoc = DB.Column(DB.Integer)
    t_numParcela = DB.Column(DB.Integer)
    t_valor = DB.Column(DB.Float)
    t_dataLanc = DB.Column(DB.String(8))
    t_dataVenc = DB.Column(DB.String(8))
    t_idCliente = DB.Column(DB.String(10), DB.ForeignKey("gf3001.c_id"))
    t_idVendedor = DB.Column(DB.String(10), DB.ForeignKey("gf3002.v_id"))
    t_saldo = DB.Column(DB.Float)
    t_status = DB.Column(DB.Boolean)
    t_docRef = DB.Column(DB.String(12))
    t_segmento = DB.Column(DB.Integer, DB.ForeignKey("gf3003.s_id"))
    t_filialOri = DB.Column(DB.Integer)
    t_filial = DB.Column(DB.Integer)
    t_ativo = DB.Column(DB.Boolean)
    t_comissao = DB.Column(DB.Float)
    
    def calculaSaldo(self, valorBaixa):
        self.t_saldo = float("%.2f"%self.t_saldo) - float("%.2f"%valorBaixa)
        if self.t_saldo == 0:
            self.t_status = 0          
    
    def estornaSaldo(self, valorStorna):
        self.t_saldo = float("%.2f"%self.t_saldo) + float("%.2f"%valorStorna)
        if self.t_saldo != 0:
            self.t_status = 1
    
    def as_dict(self):
        return {"doc": f"{self.t_docRef}"}
    
#Comissão
class Gf3005(DB.Model):
    c_id =  DB.Column(DB.Integer, primary_key=True)
    c_idVendedor = DB.Column(DB.String(10), DB.ForeignKey("gf3002.v_id"))
    c_baseCalc = DB.Column(DB.Float)
    c_idBaixa = DB.Column(DB.Integer, DB.ForeignKey("gf3006.m_id"))
    c_valor = DB.Column(DB.Float)
    c_dataBaixa = DB.Column(DB.String(8))
    c_dataPgto = DB.Column(DB.String(8))
    c_docRef = DB.Column(DB.String(12))
    c_numDoc = DB.Column(DB.Integer)
    c_perc = DB.Column(DB.Float)
    c_ativo = DB.Column(DB.Boolean)

#Movimento
class Gf3006(DB.Model):
    m_id = DB.Column(DB.Integer, primary_key=True)
    m_numDoc = DB.Column(DB.Integer)
    m_parcela = DB.Column(DB.Integer)
    m_dataBaixa = DB.Column(DB.String(8))
    m_docRef = DB.Column(DB.String(15))
    m_idCliente = DB.Column(DB.String(10), DB.ForeignKey("gf3001.c_id"))
    m_valor = DB.Column(DB.Float)
    m_tipoBaixa = DB.Column(DB.String(4))
    m_filial = DB.Column(DB.Integer)
    m_juros = DB.Column(DB.Float)
    m_deconto = DB.Column(DB.Float)
    m_observ = DB.Column(DB.String(140))
    m_usuario = DB.Column(DB.String(10))
    m_idDev = DB.Column(DB.Integer, DB.ForeignKey("gf3007.d_id"))
    m_segmento = DB.Column(DB.Integer, DB.ForeignKey("gf3003.s_id"))
    m_ativo = DB.Column(DB.Boolean)
    
    def calculaComissao(self, valor):
        valorRetorno = float(self.m_valor + self.m_juros - self.m_deconto)
        return valorRetorno * valor / 100

    def calculaBase(self):
        return float(self.m_valor + self.m_juros - self.m_deconto)

#Devolução
class Gf3007(DB.Model):
    d_id = DB.Column(DB.Integer, primary_key=True)
    d_idCliente = DB.Column(DB.String(10), DB.ForeignKey("gf3001.c_id"))
    d_valor = DB.Column(DB.Float)
    d_docRef = DB.Column(DB.String(15))
    d_dataCad = DB.Column(DB.String(8))
    d_ativo = DB.Column(DB.Boolean)
    d_saldo = DB.Column(DB.Float)
    d_status = DB.Column(DB.Boolean)
    
    def calculaCredito(self, valor):
        if self.d_saldo >= valor:
            self.d_saldo = float("%.2f"%self.d_saldo) - float("%.2f"%valor)
            if self.d_saldo == 0:
                self.d_status = 0
            return valor
        else:
            valorRetorno = float("%.2f"%self.d_saldo)
            self.d_saldo = 0 
            self.d_status = 0
            return valorRetorno
             
    def estornaCredito(self, valor):
        self.d_saldo = float("%.2f"%self.d_saldo) + float("%.2f"%valor)
        if self.d_status == 0:
            self.d_status = 1
    
    
    