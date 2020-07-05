from flask import render_template

from app.main import main
from app.utils import prepare


def render_error(message, code):
    _, kwargs = prepare()

    kwargs['message'] = message
    return render_template('error.html', **kwargs), code


# noinspection PyUnusedLocal
@main.app_errorhandler(403)
def access_denied(e):
    return render_error("403. Доступ к ресурсу запрещен", 403)


# noinspection PyUnusedLocal
@main.app_errorhandler(404)
def page_not_found(e):
    return render_error("404. Ресурс не найден", 404)


# noinspection PyUnusedLocal
@main.app_errorhandler(500)
def internal_error(e):
    return render_error("500. Внутренняя ошибка сервера", 500)
