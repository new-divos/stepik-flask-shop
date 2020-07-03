import base64
import json
import zlib

from app.main import main


@main.app_template_filter('rubles')
def _jinja2_filter_rubles(value: float):
    return f"{value:.2f} &#8381;"


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
