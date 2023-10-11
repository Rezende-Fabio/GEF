
def rotas(app):
    from ..routes.Index import indexBlue
    app.register_blueprint(indexBlue)

    from ..routes.Dashboard import dashboardBlue
    app.register_blueprint(dashboardBlue)

    from ..routes.Autenticacao import autenticacaoBlue
    app.register_blueprint(autenticacaoBlue)

    from ..routes.Erros import errosBlue
    app.register_blueprint(errosBlue)

    from ..routes.Baixa import baixaBlue
    app.register_blueprint(baixaBlue)

    from ..routes.Cliente import clienteBlue
    app.register_blueprint(clienteBlue)

    from ..routes.Devolucao import devolucaoBlue
    app.register_blueprint(devolucaoBlue)

    from ..routes.Estorno import estornoBlue
    app.register_blueprint(estornoBlue)

    from ..routes.Filtros import filtrosBlue
    app.register_blueprint(filtrosBlue)

    from ..routes.Impresao import impressaoBlue
    app.register_blueprint(impressaoBlue)

    from ..routes.Observacoes import observacaoBlue
    app.register_blueprint(observacaoBlue)

    from ..routes.Relatorio import relatorioBlue
    app.register_blueprint(relatorioBlue)

    from ..routes.Titulo import tituloBlue
    app.register_blueprint(tituloBlue)

    from ..routes.Usuario import usuarioBlue
    app.register_blueprint(usuarioBlue)

    from ..routes.Vendedor import vendedorBlue
    app.register_blueprint(vendedorBlue)