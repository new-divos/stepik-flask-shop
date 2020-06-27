from flask import Flask

from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_cls):
    app = Flask(__name__)
    app.config.from_object(config_cls)
    if hasattr(config_cls, 'init_app') and callable(config_cls.init_app):
        config_cls.init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    return app
