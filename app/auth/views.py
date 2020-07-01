from flask import (
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import login_user, logout_user

from app import db
from app.models import User
from app.auth import auth
from app.auth.forms import LoginForm, RegistrationForm


@auth.route('/login/', methods=('GET', 'POST'))
def login():
    # Словарь данных шаблона
    kwargs = dict()

    # Получить корзину из объекта сессии
    cart = session.get('cart', [])
    kwargs['cart'] = cart
    if 'cart' not in session:
        session['cart'] = cart

    # Создать форму для входа
    form = LoginForm()
    if form.validate_on_submit():
        # Найти пользователя с заданной электронной почтой
        user = db.session.query(User).filter(
            User.email == form.email.data
        ).first()
        # Если пользователь найден и проверен пароль, выполнить вход
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash("Неверные электропочта или пароль", 'error')

    kwargs['form'] = form

    return render_template('login.html', **kwargs)


@auth.route('/logout/', methods=('GET', ))
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/register/', methods=('GET', 'POST'))
def register():
    # Словарь данных шаблона
    kwargs = dict()

    # Получить корзину из объекта сессии
    cart = session.get('cart', [])
    kwargs['cart'] = cart
    if 'cart' not in session:
        session['cart'] = cart

    # Создать форму для регистрации
    form = RegistrationForm()
    if form.validate_on_submit():
        # Создать нового пользователя
        # noinspection PyArgumentList
        user = User(email=form.email.data)
        user.password = form.password.data

        db.session.add(user)
        db.session.commit()

        flash("Спасибо за регистрацию", 'info')
        return redirect(url_for('auth.login'))

    kwargs['form'] = form

    return render_template('register.html', **kwargs)
