from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length


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
