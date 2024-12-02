import stripe
from decouple import config

stripe.api_key = config('API_KEY_STRIPE')


def create_product(product):
    """ Создание продукта """
    starter_subscription = stripe.Product.create(
        name=product
    )
    return starter_subscription


def create_price(product, price):
    """ Создание стоимости продукта """
    rub_price = stripe.Price.create(
        product=product.get('id'),
        currency="rub",
        unit_amount=price * 100
    )
    return rub_price


def create_session(price):
    """ Создание сессии на оплату """
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')


def get_status_session(session_id):
    """ Получение сессии """
    session = stripe.checkout.Session.retrieve(session_id)
    return session


def create_refund(session_id):
    """ Создание возврата """
    if get_status_session(session_id).payment_status == "paid":
        refund = stripe.Refund.create(
            charge=session_id
        )
        return refund
