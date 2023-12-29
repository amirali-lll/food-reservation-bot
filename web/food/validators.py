from django.core.exceptions import ValidationError
from django.conf import settings
from .models import Order 




MAX_ORDERS_PRICE = settings.MAX_ORDERS_PRICE


# validate order price under MAX_ORDERS_PRICE
def validate_order_price(current_order :Order, new_order_price :int):
    current_order_price = new_order_price
    if current_order:
        current_order_price += current_order.get_price()
    if current_order_price > MAX_ORDERS_PRICE:
        raise ValidationError(f'قیمت سفارش شما بیشتر از {MAX_ORDERS_PRICE} تومان است')
    return True
    