from flask_login import LoginManager


def init_app(app):
    login_manager = LoginManager()
    login_manager.login_view = 'errosBlue.methodNOTALLOWED'
    login_manager.login_message = False
    login_manager.init_app(app)
    
    from ..models.Models import SysUsers
    @login_manager.user_loader
    def load_user(id):
        return SysUsers.query.filter(SysUsers.id == id, SysUsers.s_ativo != False).first()