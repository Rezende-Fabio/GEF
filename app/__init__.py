from flask import Flask

app = Flask(__name__)
from app import config
from app.routes import Baixa, Cliente, Devolucao, Estorno, Filtros, Impresao, Main, Observacoes, Relatorio, Titulo, Usuario, Vendedor
