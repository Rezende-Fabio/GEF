from ..controllers.ControllerConsultas import consultaAtraso
from ..controllers.ControllerVendedor import ControllerVendedor
from ..extensions.integracao import Atualizacao
from flask import Blueprint, g

vendedorBlue = Blueprint("vendedorBlue", __name__, url_prefix="/vendedor")
controleVendedor = ControllerVendedor()

@vendedorBlue.before_request
def before_request():   
    g.qtdeAtraso = consultaAtraso()
    g.integracao = Atualizacao()
    g.maxCli, g.maxVend = g.integracao.qtdeCliVend()


vendedorBlue.add_url_rule("/lista-vendedores", "renderListaVendedores", controleVendedor.renderListaVendedores, "", methods=["GET"])
vendedorBlue.add_url_rule("/<idVend>", "renderConsultarVendedor", controleVendedor.renderConsultarVendedor, "", methods=["GET"])
vendedorBlue.add_url_rule("/atualiza-baseVend", "atualizarBaseVendedor", controleVendedor.atulizarBaseVendedor, "", methods=["GET"])
vendedorBlue.add_url_rule("/atualiza-baseVend-redirect", "atualizarBaseVendedorRedirect", controleVendedor.atulizarBaseVendedorRedirect, "", methods=["GET"])
vendedorBlue.add_url_rule("/vendedores/<pesquisa>", "pesquisaAutocomplete", controleVendedor.pesquisarVendedoresAutocomplete, "", methods=["GET"])
vendedorBlue.add_url_rule("/vendedores", "consultarVendedores", controleVendedor.consultarVendedores, "", methods=["GET"])   
vendedorBlue.add_url_rule("/verifica-vendedor/<idVend>", "verificarVendedor", controleVendedor.verificarVendedor, "", methods=["GET"])
    