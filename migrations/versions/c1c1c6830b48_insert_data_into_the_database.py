"""Insert data into the database

Revision ID: c1c1c6830b48
Revises: 3e51d222067d
Create Date: 2020-06-30 21:15:46.683539

"""
from pathlib import Path

from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
import xlrd


# revision identifiers, used by Alembic.
revision = 'c1c1c6830b48'
down_revision = '3e51d222067d'
branch_labels = None
depends_on = None

Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(120), unique=True, index=True)


class Meal(Base):
    __tablename__ = 'meals'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(180), unique=True, index=True)
    price = sa.Column(sa.Float, nullable=False, default=0.0)
    description = sa.Column(sa.Text)
    picture = sa.Column(sa.String(80))
    category_id = sa.Column(sa.Integer, sa.ForeignKey('categories.id'))


def upgrade():
    book = xlrd.open_workbook(
        Path(__file__).parent.parent.parent / "data" / "data.xlsx"
    )

    meals_sheet = book.sheet_by_name('meals')
    categories_sheet = book.sheet_by_name('categories')

    bind = op.get_bind()
    session = orm.Session(bind=bind)

    for rowx in range(1, categories_sheet.nrows):
        if categories_sheet.row_len(rowx) >= 2:
            row = categories_sheet.row_values(rowx)
            session.add(
                Category(
                    id=row[0],
                    title=row[1]
                )
            )

    for rowx in range(1, meals_sheet.nrows):
        if meals_sheet.row_len(rowx) >= 6:
            row = meals_sheet.row_values(rowx)
            session.add(
                Meal(
                    id=row[0],
                    title=row[1],
                    price=float(row[2]),
                    description=row[3],
                    picture=row[4],
                    category_id=row[5]
                )
            )

    session.commit()


def downgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    for meal in session.query(Meal).all():
        session.delete(meal)

    for category in session.query(Category).all():
        session.delete(category)

    session.commit()
