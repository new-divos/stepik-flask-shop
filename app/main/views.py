from flask import (
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    send_from_directory,
    url_for,
)

from app.main import main


@main.route('/')
@main.route('/index/')
def index():
    return "Hello"


@main.route('/static/<path:filename>')
def staticfiles(filename):
    return send_from_directory(current_app.config['APP_STATIC_DIR'], filename)
