
def rotas(app):
    from ..routes.Index import indexBlue
    app.register_blueprint(indexBlue)

    from ..routes.DashboardRoute import dashboardBlue
    app.register_blueprint(dashboardBlue)

    from ..routes.AutenticacaoRoute import autenticacaoBlue
    app.register_blueprint(autenticacaoBlue)

    from ..routes.Erros import errosBlue
    app.register_blueprint(errosBlue)

    from ..routes.Baixa import baixaBlue
    app.register_blueprint(baixaBlue)

    from ..routes.ClienteRoute import clienteBlue
    app.register_blueprint(clienteBlue)

    from ..routes.Devolucao import devolucaoBlue
    app.register_blueprint(devolucaoBlue)

    from ..routes.Estorno import estornoBlue
    app.register_blueprint(estornoBlue)

    from ..routes.Filtros import filtrosBlue
    app.register_blueprint(filtrosBlue)

    from ..routes.Impresao import impressaoBlue
    app.register_blueprint(impressaoBlue)

    from ..routes.ObservacoesRoute import observacaoBlue
    app.register_blueprint(observacaoBlue)

    from ..routes.RelatorioRoute import relatorioBlue
    app.register_blueprint(relatorioBlue)

    from ..routes.TituloRoute import tituloBlue
    app.register_blueprint(tituloBlue)

    from ..routes.UsuarioRoute import usuarioBlue
    app.register_blueprint(usuarioBlue)

    from ..routes.VendedorRoute import vendedorBlue
    app.register_blueprint(vendedorBlue)