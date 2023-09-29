from flask_sqlalchemy import SQLAlchemy
from tomli import load
import os

DB = SQLAlchemy()

def init_app(app):
    settings = load(open('settings.toml', 'rb'))
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    database_path = os.path.join(project_dir, settings['database']['relative_path'])
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'

    DB.init_app(app)