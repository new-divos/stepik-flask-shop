from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Email, Length, EqualTo

from app import db
from app.models import User


class LoginForm(FlaskForm):
    email = StringField(
        "Электропочта",
        id='inputEmail',
        validators=[InputRequired(), Length(1, 64), Email()]
    )
    password = PasswordField(
        "Пароль",
        id='inputPassword',
        validators=[InputRequired()]
    )
    submit = SubmitField("Войти")


class RegistrationForm(FlaskForm):
    email = StringField(
        "Электропочта",
        id='inputEmail',
        validators=[InputRequired(), Length(1, 64), Email()]
    )
    password = PasswordField(
        "Пароль",
        id='inputPassword',
        validators=[
            InputRequired(),
            EqualTo(
                'password2',
                message="Пароли должны совпадать"
            )
        ]
    )
    password2 = PasswordField(
        "Пароль еще раз",
        id='inputPassword2',
        validators=[InputRequired()]
    )
    submit = SubmitField("Зарегистрироваться")

    def validate_email(self, field):
        if db.session.query(User).filter(User.email == field.data).first():
            raise ValidationError(
                f"Пользователь с такой электропочтой уже зарегистрирован"
            )

