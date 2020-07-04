import base64
from datetime import datetime
import json
import zlib

from app.main import main

months = (
    "Января",
    "Февраля",
    "Марта",
    "Апреля",
    "Мая",
    "Июня",
    "Июля",
    "Августа",
    "Сентября",
    "Ноября",
    "Декабря"
)


@main.app_template_filter('rubles')
def _jinja2_filter_rubles(value: float):
    return f"{value:.2f}&nbsp;&#8381;"


@main.app_template_filter('total')
def _jinja2_filter_total(cart: list):
    result = 0.0
    for item in cart:
        result += item.get('price', 0.0) * item.get('amount', 0)
    return result


@main.app_template_filter('dishes')
def _jinja2_filter_dishes(value: int):
    value = abs(value)
    r10, r100 = value % 10, value % 100

    if r10 == 1 and not 10 < r100 < 20:
        name = "блюдо"
    elif 1 < r10 < 5 and not 10 < r100 < 20:
        name = "блюда"
    else:
        name = "блюд"

    return f"{value} {name}"


@main.app_template_filter('compress')
def _jinja2_filter_compress(cart: list):
    data = json.dumps([(item['id'], item.get('amount', 0)) for item in cart])
    return base64.b64encode(
        zlib.compress(data.encode('UTF-8'))
    ).decode('UTF-8')


@main.app_template_filter('format_date')
def _jinja2_filter_date_fmt(date: datetime):
    global months
    return "{} {} {} г. {}:{}".format(
        date.day,
        months[date.month - 1],
        date.year,
        date.hour,
        date.minute
    )


@main.app_template_filter('format_short_date')
def _jinja2_filter_format_short_date(date: datetime):
    return date.strftime("%Y-%m-%d %H:%M")
