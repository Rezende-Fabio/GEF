from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Column, String, DateTime, Boolean, Float, Integer, Numeric, ForeignKey
from app import app
import os
from werkzeug.security import check_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'GefIII.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Usuários
class SysUsers(db.Model):
    s_codigo = db.Column(db.Integer, primary_key=True)
    s_usuario = db.Column(db.String(10))
    s_senha = db.Column(db.String(32))
    s_nome = db.Column(db.String(80))
    s_email = db.Column(db.String(80), unique=True)
    s_admin = db.Column(db.Boolean)
    s_ativo = db.Column(db.Boolean)
    s_novaSenha = db.Column(db.Boolean)
    
    def __repr__(self):
        return f"{self.s_codigo}"
    
    def verificaSenha(self, senha):
        return check_password_hash(self.s_senha, senha)

#Cliente
class Gf3001(db.Model):
    c_id = db.Column(db.String(10), primary_key=True)
    c_codigo = db.Column(db.String(9))
    c_loja = db.Column(db.String(2))
    c_razaosocial = db.Column(db.String(45))
    c_cpfcnpj = db.Column(db.String(14))
    c_inscricao = db.Column(db.String(18))
    c_email = db.Column(db.String(45))
    c_endereco = db.Column(db.String(60))
    c_bairro = db.Column(db.String(30))
    c_cep = db.Column(db.String(9))
    c_cidade = db.Column(db.String(40))
    c_uf = db.Column(db.String(18))
    c_telefone = db.Column(db.String(11))
    c_codvend = db.Column(db.String(6))
    c_dataCriacao = db.Column(db.String(8))
    c_ativo = db.Column(db.Boolean)
    
    def as_dict(self):
        return {"nome": f"{self.c_id} - {self.c_razaosocial}"}

#Vendedor
class Gf3002(db.Model):
    v_id = db.Column(db.String(10), primary_key=True)
    v_nome = db.Column(db.String(45))
    v_endereco = db.Column(db.String(60))
    v_bairro = db.Column(db.String(30))
    v_cidade = db.Column(db.String(40))
    v_uf = db.Column(db.String(18))
    v_cep = db.Column(db.String(9))
    v_contato = db.Column(db.String(45))
    v_cpfcnpj = db.Column(db.String(14))
    v_inscricao = db.Column(db.String(18))
    v_telefone = db.Column(db.String(11))
    v_celular = db.Column(db.String(11))
    v_comis = db.Column(db.Float)
    v_email = db.Column(db.String(45))
    v_ativo = db.Column(db.Boolean)
    
    def as_dict(self):
        return {"nome": f"{self.v_id} - {self.v_nome}"}

#Seguimentos
class Gf3003(db.Model):
    s_id = db.Column(db.Integer, primary_key=True)
    s_desc = db.Column(db.String(40))
    s_abrev = db.Column(db.String(5))
    s_filial = db.Column(db.Integer)
    
    def __repr__(self):
        return f"{self.s_abrev}"

#Titulo   
class Gf3004(db.Model):
    t_id = db.Column(db.Integer, primary_key=True)
    t_numDoc = db.Column(db.Integer)
    t_numParcela = db.Column(db.Integer)
    t_valor = db.Column(db.Float)
    t_dataLanc = db.Column(db.String(8))
    t_dataVenc = db.Column(db.String(8))
    t_idCliente = db.Column(db.String(10), db.ForeignKey("gf3001.c_id"))
    t_idVendedor = db.Column(db.String(10), db.ForeignKey("gf3002.v_id"))
    t_saldo = db.Column(db.Float)
    t_status = db.Column(db.Boolean)
    t_docRef = db.Column(db.String(12))
    t_segmento = db.Column(db.Integer, db.ForeignKey("gf3003.s_id"))
    t_filialOri = db.Column(db.Integer)
    t_filial = db.Column(db.Integer)
    t_ativo = db.Column(db.Boolean)
    t_comissao = db.Column(db.Float)
    
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
class Gf3005(db.Model):
    c_id =  db.Column(db.Integer, primary_key=True)
    c_idVendedor = db.Column(db.String(10), db.ForeignKey("gf3002.v_id"))
    c_baseCalc = db.Column(db.Float)
    c_idBaixa = db.Column(db.Integer, db.ForeignKey("gf3006.m_id"))
    c_valor = db.Column(db.Float)
    c_dataBaixa = db.Column(db.String(8))
    c_dataPgto = db.Column(db.String(8))
    c_docRef = db.Column(db.String(12))
    c_numDoc = db.Column(db.Integer)
    c_perc = db.Column(db.Float)
    c_ativo = db.Column(db.Boolean)

#Movimento
class Gf3006(db.Model):
    m_id = db.Column(db.Integer, primary_key=True)
    m_numDoc = db.Column(db.Integer)
    m_parcela = db.Column(db.Integer)
    m_dataBaixa = db.Column(db.String(8))
    m_docRef = db.Column(db.String(15))
    m_idCliente = db.Column(db.String(10), db.ForeignKey("gf3001.c_id"))
    m_valor = db.Column(db.Float)
    m_tipoBaixa = db.Column(db.String(4))
    m_filial = db.Column(db.Integer)
    m_juros = db.Column(db.Float)
    m_deconto = db.Column(db.Float)
    m_observ = db.Column(db.String(140))
    m_usuario = db.Column(db.String(10))
    m_idDev = db.Column(db.Integer, db.ForeignKey("gf3007.d_id"))
    m_segmento = db.Column(db.Integer, db.ForeignKey("gf3003.s_id"))
    m_ativo = db.Column(db.Boolean)
    
    def calculaComissao(self, valor):
        valorRetorno = float(self.m_valor + self.m_juros - self.m_deconto)
        return valorRetorno * valor / 100

    def calculaBase(self):
        return float(self.m_valor + self.m_juros - self.m_deconto)

#Devolução
class Gf3007(db.Model):
    d_id = db.Column(db.Integer, primary_key=True)
    d_idCliente = db.Column(db.String(10), db.ForeignKey("gf3001.c_id"))
    d_valor = db.Column(db.Float)
    d_docRef = db.Column(db.String(15))
    d_dataCad = db.Column(db.String(8))
    d_ativo = db.Column(db.Boolean)
    d_saldo = db.Column(db.Float)
    d_status = db.Column(db.Boolean)
    
    def calculaCredito(self, valor):
        if self.d_saldo >= valor:
            self.d_saldo = float("%.2f"%self.d_saldo) - float("%.2f"%valor)
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
    
    
    