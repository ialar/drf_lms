import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(instance):
    """Создание продукта в stripe."""
    product_name = f"{instance.paid_course.name}" if instance.paid_course else f"{instance.paid_lesson.name}"
    stripe_product = stripe.Product.create(name=f'{product_name}')
    return stripe_product.id


def create_stripe_price(product_id, payment):
    """Создание цены продукта в stripe."""
    price = stripe.Price.create(product=product_id, currency="rub", unit_amount=payment.amount * 100)
    return price.id


def create_stripe_session(price_id):
    """Создание сессии оплаты в stripe."""
    session = stripe.checkout.Session.create(
        success_url="http://localhost:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url
