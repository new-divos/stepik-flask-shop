from flask_wtf import FlaskForm
import phonenumbers
from wtforms import HiddenField, StringField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Email, Length


class OrderForm(FlaskForm):
    name = StringField(
        "Ваше имя",
        id='inputName',
        validators=[
            InputRequired(),
            Length(
                1,
                120,
                message="Длина имени должна быть от 1 до 120 символа"
            )
        ]
    )
    address = StringField(
        "Адрес",
        id='inputAddress',
        validators=[
            InputRequired(),
            Length(
                1,
                200,
                message="Длина адреса должна быть от 1 до 200 символа"
            )
        ]
    )
    email = StringField(
        "Электропочта",
        id='inputEmail',
        validators=[
            InputRequired(),
            Length(
                1,
                80,
                message="Длина электропочты должна быть от 1 до 80 символов"
            ),
            Email(
                message="Неверный формат электропочты"
            )
        ]
    )
    phone = StringField(
        "Телефон",
        id="inputPhone",
        validators=[
            InputRequired(),
            Length(
                1,
                20,
                message="Длина телефона должна быть от 1 до 20 символов"
            )
        ]
    )
    cart = HiddenField(
        "Корзина",
        id='cart',
        validators=[InputRequired()],
    )
    submit = SubmitField("Оформить заказ")

    def validate_phone(self, field):
        try:
            p = phonenumbers.parse(field.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (
            phonenumbers.phonenumberutil.NumberParseException,
            ValueError
        ):
            raise ValidationError("Неверный номер телефона")
