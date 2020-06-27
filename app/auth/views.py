from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_user, logout_user

from app import db
from app.models import User
from app.auth import auth
from app.auth.forms import LoginForm


@auth.route('/login/', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(
            User.email == form.email.data
        ).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash("Неверные электропочта или пароль", 'error')

    return render_template('login.html', form=form)


@auth.route('/logout/', methods=('GET', ))
def logout():
    logout_user()
    return redirect(url_for('main.index'))
