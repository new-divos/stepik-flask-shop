from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import InputRequired, EqualTo


class ChangePasswordForm(FlaskForm):
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
    submit = SubmitField("Изменить пароль")
