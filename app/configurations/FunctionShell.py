from .DataBase import DB

def function_shell(app):
    
    @app.cli.command("create_db")
    def create_db():
        with app.app_context():
            DB.create_all()
            # insereParametros()


    @app.cli.command("drop_db")
    def drop_db():
        with app.app_context():
            DB.drop_all()