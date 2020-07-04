from flask import (
    abort,
    current_app,
    flash,
    render_template,
    redirect,
    request,
    url_for
)
from flask_login import current_user
from flask_paginate import get_page_parameter, Pagination

from app import db
from app.admin import admin
from app.admin.forms import ChangePasswordForm
from app.models import (
    Category,
    Meal,
    User,
)
from app.utils import prepare, superuser_required


@admin.route('/categories/', methods=('GET', ))
@superuser_required
def render_meals():
    _, kwargs = prepare()

    # Получить категорию, если она задана
    category_id = request.args.get('category', type=int, default=0)
    if category_id > 0:
        category = db.session.query(Category).get_or_404(category_id)
    else:
        category = None
    kwargs['category'] = category

    # Получить число заказов на странице
    per_page = current_app.config['ADMIN_ROWS_PER_PAGE'] or 10

    # Получить число блюд на странице
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * per_page

    # Получить список блюд
    if category:
        meals = db.session.query(Meal).filter(
            Meal.category_id == category_id
        ).order_by(Meal.title).all()
    else:
        meals = db.session.query(Meal).order_by(Meal.title).all()
    kwargs['meals'] = meals[offset:offset + per_page]

    # Создать пажинатор
    pagination = Pagination(
        page=page,
        total=len(meals),
        per_page=per_page,
        offset=offset,
        record_name='meals',
        bs_version=4
    )
    kwargs['pagination'] = pagination

    return render_template('meals.html', **kwargs)


@admin.route('/meals/', methods=('GET', ))
@superuser_required
def render_categories():
    _, kwargs = prepare()

    # Получить число заказов на странице
    per_page = current_app.config['ADMIN_ROWS_PER_PAGE'] or 10

    # Получить число блюд на странице
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * per_page

    # Получить список категорий
    categories = db.session.query(Category).order_by(Category.title).all()
    kwargs['categories'] = categories[offset:offset + per_page]

    # Создать пажинатор
    pagination = Pagination(
        page=page,
        total=len(categories),
        per_page=per_page,
        offset=offset,
        record_name='categories',
        bs_version=4
    )
    kwargs['pagination'] = pagination

    return render_template('categories.html', **kwargs)


@admin.route('/users/', methods=('GET', ))
@superuser_required
def render_users():
    _, kwargs = prepare()

    # Получить число заказов на странице
    per_page = current_app.config['ADMIN_ROWS_PER_PAGE'] or 10

    # Получить число блюд на странице
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * per_page

    # Получить список пользователей
    users = db.session.query(User).all()
    kwargs['users'] = users[offset:offset + per_page]

    # Создать пажинатор
    pagination = Pagination(
        page=page,
        total=len(users),
        per_page=per_page,
        offset=offset,
        record_name='users',
        bs_version=4
    )
    kwargs['pagination'] = pagination

    return render_template('users.html', **kwargs)


@admin.route('/users/remove/<int:id>/')
@superuser_required
def remove_user(id):
    # Нельзя удалить текущего пользователя
    if current_user.id == id:
        abort(403)

    # Получить пользователя с заданным идентификатором
    user = db.session.query(User).get_or_404(id)
    email = user.email

    # Удалить пользователя
    db.session.delete(user)
    db.session.commit()

    flash(f"Пользователь {email} был удален", 'warning')
    return redirect(url_for('admin.render_users'))


@admin.route('/users/grant/<int:id>/')
@superuser_required
def grant_user(id):
    # Получить пользователя с заданным идентификатором
    user = db.session.query(User).get_or_404(id)

    # Нельзя повысить права суперпользователя
    if user.is_superuser:
        abort(403)

    # Установить права суперпользователя
    user.is_superuser = True
    db.session.commit()

    flash(f"Пользователь {user.email} был повышен в правах", 'warning')
    return redirect(url_for('admin.render_users'))


@admin.route('/users/revoke/<int:id>/')
@superuser_required
def revoke_user(id):
    # Получить пользователя с заданным идентификатором
    user = db.session.query(User).get_or_404(id)

    # Нельзя понизить права обычного пользователя и
    # текущего пользователя
    if not user.is_superuser or current_user.id == id:
        abort(403)

    # Отозвать права суперпользователя
    user.is_superuser = False
    db.session.commit()

    flash(f"Пользователь {user.email} был понижен в правах", 'warning')
    return redirect(url_for('admin.render_users'))


@admin.route('/users/change_pass/<int:id>/', methods=('GET', 'POST'))
@superuser_required
def change_password(id):
    _, kwargs = prepare()

    # Получить пользователя с заданным идентификатором
    user = db.session.query(User).get_or_404(id)
    kwargs['user'] = user

    # Создать форму для изменения пароля
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()

        flash(f"Пароль пользователя {user.email} был изменен", 'warning')
        return redirect(url_for('admin.render_users'))

    kwargs['form'] = form
    return render_template('change_password.html', **kwargs)
