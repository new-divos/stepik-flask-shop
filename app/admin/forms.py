from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        "Пароль",
        id='inputPassword',
        validators=[
            DataRequired(),
            EqualTo(
                'password2',
                message="Пароли должны совпадать"
            )
        ]
    )
    password2 = PasswordField(
        "Пароль еще раз",
        id='inputPassword2',
        validators=[DataRequired()]
    )
    submit = SubmitField("Изменить пароль")
