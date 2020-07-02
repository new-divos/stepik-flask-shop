from functools import wraps

from flask import abort, session
from flask_login import current_user


def superuser_required(f):
    """
    Требует права суперпользователя для роута
    :param f: обертываемая функция роута
    :return: функция роута после обертки
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_superuser:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


def prepare():
    """
    Подготовливает данные для работы с карзиной
    :return: кортеж из двух элементов: первым является список
    элементов корзины, а вторым словарь аргументов шаблона
    """
    # Словарь данных шаблона
    kwargs = dict()

    # Получить корзину из объекта сессии
    cart = session.get('cart', [])
    kwargs['cart'] = cart
    if 'cart' not in session:
        session['cart'] = cart

    return cart, kwargs
