from collections import OrderedDict, namedtuple

from flask import (
    abort,
    current_app,
    flash,
    redirect,
    request,
    render_template,
    send_from_directory,
    session,
    url_for,
)
from sqlalchemy.sql.expression import func

from app import db
from app.main import main
from app.main.forms import OrderForm
from app.models import (
    Category,
    Meal,
)
from app.toolkit import prepare


# Ключ словаря с группированными по категорям данными
CategoryKey = namedtuple('CategoryItem', ('id', 'title'))


@main.route('/')
@main.route('/index/')
def index():
    _, kwargs = prepare()

    # Построить словарь с разделением по категориям
    categorized = OrderedDict()

    categories = db.session.query(Category).order_by(Category.title).all()
    for category in categories:
        # Запросить 3 рандомных блюда по данной категории
        # и отсортировать их по имени
        meals = sorted(
            db.session.query(Meal).filter(
                Meal.category == category
            ).order_by(func.random()).limit(3),
            key=lambda item: item.title
        )
        # Добавить список выбранных блюд в словарь.
        categorized[
            CategoryKey(
                id=category.id,
                title=category.title
            )
        ] = meals

        kwargs['categorized'] = categorized

    return render_template('main.html', **kwargs)


@main.route('/category/<int:id>')
def render_category(id):
    _, kwargs = prepare()

    # Получить категорию по индексу
    kwargs['category'] = db.session.query(Category).get_or_404(id)

    # Получить отсортированный список блюд данной категории
    kwargs['meals'] = db.session.query(Meal).filter(
        Meal.category_id == id
    ).order_by(Meal.title)

    return render_template('category.html', **kwargs)


@main.route('/addtocart/<int:id>/<int:amount>')
def add_to_cart(id, amount):
    cart, _ = prepare()

    # Если требуемое количество неположительно, то выдать ошибку 404
    if amount <= 0:
        abort(404)

    # Выполнить поиск требуемого блюда
    meal = db.session.query(Meal).get_or_404(id)

    # Добавить блюдо в карзину
    cart.append(
        dict(
            id=meal.id,
            title=meal.title,
            price=meal.price,
            amount=amount
        )
    )

    # Записать результат в сессию
    session['cart'] = cart

    # Переход на предыдущую страницу
    return redirect(request.referrer or url_for('main.index'))


@main.route('/cart/')
def render_cart():
    cart, kwargs = prepare()

    form = OrderForm()

    kwargs['form'] = form

    return render_template('cart.html', **kwargs)


@main.route('/static/<path:filename>')
def staticfiles(filename):
    return send_from_directory(current_app.config['APP_STATIC_DIR'], filename)
