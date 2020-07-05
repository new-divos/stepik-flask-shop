from enum import Enum

from flask import url_for
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.sql.functions import now

from app import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, index=True)

    meals = db.relationship(
        'Meal',
        back_populates='category',
        cascade='all,delete',
        lazy='dynamic'
    )

    @hybrid_method
    def count_meals(self):
        return len(tuple(self.meals))


class Meal(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), unique=True, index=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    description = db.Column(db.Text)
    picture = db.Column(db.String(80))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    category = db.relationship(
        'Category',
        uselist=False,
        back_populates='meals'
    )
    positions = db.relationship(
        'OrderPosition',
        back_populates='meal',
        cascade='all,delete',
        lazy='dynamic'
    )

    @hybrid_method
    def picture_url(self):
        return url_for(
            'static',
            filename=f"images/{self.picture}"
        )


class OrderStatus(Enum):
    CREATED = "Создан"
    READY = "Готов"
    DELIVERED = "Доставлен"


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=now())
    total = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(
        db.Enum(OrderStatus),
        nullable=False,
        default=OrderStatus.CREATED
    )
    name = db.Column(db.String(120))
    address = db.Column(db.String(200))
    email = db.Column(db.String(80))
    phone = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship(
        'User',
        uselist=False,
        back_populates='orders',
    )
    positions = db.relationship(
        'OrderPosition',
        back_populates='order',
        cascade='all,delete',
        lazy='dynamic'
    )

    @hybrid_method
    def get_total(self):
        return sum(position.cost for position in self.positions)


class OrderPosition(db.Model):
    __tablename__ = 'orders_positions'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'))
    amount = db.Column(db.Integer, nullable=False, default=0)

    order = db.relationship(
        'Order',
        uselist=False,
        back_populates='positions'
    )
    meal = db.relationship(
        'Meal',
        uselist=False,
        back_populates='positions'
    )

    @hybrid_property
    def cost(self):
        return self.meal.price * self.amount
