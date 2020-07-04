#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import getpass
import logging
import os
import re

from flask.cli import FlaskGroup

from app import create_app, db
from app.config import config
from app.models import (
    Category,
    Meal,
    OrderStatus,
    Order,
    OrderPosition,
    User,
)


current_config = config.get(os.getenv('FLASK_ENV'))
if current_config is None:
    raise RuntimeError(
        "unknown configuration, check FLASK_ENV environment variable value"
    )

app = create_app(current_config)
cli = FlaskGroup(app)


@app.shell_context_processor
def make_shell_context():
    return dict(
        app=app,
        db=db,
        Category=Category,
        Meal=Meal,
        OrderStatus=OrderStatus,
        Order=Order,
        OrderPosition=OrderPosition,
        User=User,
    )


# Команда для создания суперпользователя
@app.cli.command('create-superuser')
def create_superuser():
    superuser = db.session.query(User).filter(User.is_superuser).first()
    if superuser is None:
        email = input("Enter the superuser email: ")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            logging.error(f"Illegal email {email} for the superuser")
            return

        try:
            # Ввод пароля суперпользователя
            password = getpass.getpass(
                prompt="Enter the superuser password: "
            )

            # Повторный ввод пароля суперпользователя
            password2 = getpass.getpass(
                prompt="Enter the superuser password again: "
            )

        except Exception as e:
            logging.error(f"The superuser password cannot be retrieved {e}")
            return

        else:
            if not password or not password2:
                logging.error("The superuser password cannot be empty")
                return

        if password != password2:
            logging.error("The entered passwords are mismatch")
            return

        # noinspection PyArgumentList
        superuser = User(email=email, is_superuser=True)
        superuser.password = password

        db.session.add(superuser)
        db.session.commit()

        logging.info("The superuser successfully created")

    else:
        logging.error("The superuser is already exist")


if __name__ == '__main__':
    cli()
