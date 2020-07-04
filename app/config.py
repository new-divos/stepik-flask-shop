import os
from pathlib import Path


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', ":'(")
    # Путь к статическим файлам
    APP_STATIC_DIR = Path(
        os.getenv(
            'APP_STATIC_DIR',
            str(Path(__file__).parent / 'app' / 'static')
        )
    )
    DATABASE_URL = os.getenv(
        'DATABASE_URL',
        f"sqlite:///{Path(__file__).parent.parent / 'data.db'}"
    )
    # Количество заказов на одной стринице в личном кабинете пользователя
    ORDERS_PER_PAGE = int(os.getenv('ORDERS_PER_PAGE', '1'))
    # Количество строк в таблицах для административных страниц
    ADMIN_ROWS_PER_PAGE = int(os.getenv('ADMIN_ROWS_PER_PAGE', '10'))

    @classmethod
    def init_app(cls, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URL']
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
