from flask import current_app, render_template, request
from flask_paginate import get_page_parameter, Pagination

from app import db
from app.admin import admin
from app.models import (
    Category,
    Meal,
)
from app.utils import prepare, superuser_required


@admin.route('/categories/')
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

    # Получить пажинатор
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


@admin.route('/meals/')
@superuser_required
def render_categories():
    _, kwargs = prepare()

    # Получить число заказов на странице
    per_page = current_app.config['ADMIN_ROWS_PER_PAGE'] or 10

    # Получить число блюд на странице
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * per_page

    # Получить список блюд
    categories = db.session.query(Category).order_by(Category.title).all()
    kwargs['categories'] = categories[offset:offset + per_page]

    # Получить пажинатор
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
