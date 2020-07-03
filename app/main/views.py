import base64
from collections import OrderedDict, namedtuple
import json
import zlib

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
from flask_login import current_user, login_required
from sqlalchemy.sql.expression import func

from app import db
from app.main import main
from app.main.forms import OrderForm
from app.models import (
    Category,
    Meal,
    Order,
    OrderPosition,
)
from app.utils import prepare, save_path


# Ключ словаря с группированными по категорям данными
CategoryKey = namedtuple('CategoryItem', ('id', 'title'))


@main.route('/', methods=('GET', ))
@main.route('/index/', methods=('GET', ))
@save_path
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


@main.route('/category/<int:id>/', methods=('GET', ))
@save_path
def render_category(id):
    _, kwargs = prepare()

    # Получить категорию по индексу
    kwargs['category'] = db.session.query(Category).get_or_404(id)

    # Получить отсортированный список блюд данной категории
    kwargs['meals'] = db.session.query(Meal).filter(
        Meal.category_id == id
    ).order_by(Meal.title)

    return render_template('category.html', **kwargs)


@main.route('/addtocart/<int:id>/<int:amount>/', methods=('GET', ))
def add_to_cart(id, amount):
    cart, _ = prepare()

    # Если требуемое количество неположительно, то выдать ошибку 404
    if amount <= 0:
        abort(404)

    # Выполнить поиск требуемого блюда в БД
    meal = db.session.query(Meal).get_or_404(id)

    # Добавить блюдо в корзину
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


@main.route('/removefromcart/<int:position>/')
def remove_from_cart(position):
    cart, _ = prepare()

    if position <= 0 or position > len(cart):
        abort(404)

    del cart[position - 1]
    session['cart'] = cart

    flash("Блюдо удалено из корзины", 'warning')

    return redirect(url_for('main.render_cart'))


@main.route('/cart/', methods=('GET', 'POST'))
@save_path
def render_cart():
    cart, kwargs = prepare()

    form = OrderForm()
    kwargs['form'] = form

    if form.validate_on_submit():
        # Создать объект заказа
        order = Order(
            total=float(form.order_total.data),
            name=form.name.data,
            address=form.address.data,
            email=form.email.data,
            phone=form.phone.data,
            user=current_user,
        )
        db.session.add(order)

        # Получить данные корзины из формы
        form_cart = json.loads(
            zlib.decompress(
                base64.b64decode(
                    form.order_cart.data.encode('utf-8')
                )
            ).decode('utf-8')
        )

        if not form_cart:
            db.session.rollback()
            abort(404)

        # Выбрать сведения о блюдах из базы данных
        meals = db.session.query(Meal).filter(
            Meal.id.in_(set(item[0] for item in form_cart))
        ).all()

        # Создать записи о позициях заказа
        for item in form_cart:
            meal = next(
                (m for m in meals if m.id == item[0]),
                None
            )

            if not meal:
                db.session.rollback()
                abort(404)

            position = OrderPosition(
                order=order,
                meal=meal,
                amount=item[1]
            )
            db.session.add(position)

        db.session.commit()
        session['cart'] = []

        return redirect(url_for('main.render_ordered'))

    return render_template('cart.html', **kwargs)


@main.route('/ordered/', methods=('GET', ))
@login_required
def render_ordered():
    return render_template('ordered.html')


@main.route('/static/<path:filename>', methods=('GET', ))
def staticfiles(filename):
    return send_from_directory(current_app.config['APP_STATIC_DIR'], filename)
