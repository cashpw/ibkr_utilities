from typing import Callable
from decimal import Decimal, ROUND_HALF_DOWN
from ibkr_utilities.util.is_call import is_call

def calc_put_value(underlying_price: Decimal, strike_price: Decimal, multiplier: int) -> Decimal:
    if underlying_price >= strike_price:
        return 0

    value = Decimal((strike_price - underlying_price) * multiplier)
    return Decimal(value.quantize(Decimal('.01'), rounding=ROUND_HALF_DOWN))

def calc_call_value(underlying_price: Decimal, strike_price: Decimal, multiplier: int) -> Decimal:
    if underlying_price <= strike_price:
        return 0

    value = Decimal((underlying_price - strike_price) * multiplier)
    return Decimal(value.quantize(Decimal('.01'), rounding=ROUND_HALF_DOWN))


def build_option_value_fn(strike_price: Decimal, right: str, multiplier=100) -> Callable[[Decimal], Decimal]:
    if is_call(right):
        return lambda underlying_price: calc_call_value(
            underlying_price=underlying_price,
            strike_price=strike_price,
            multiplier=multiplier,
        )
    else:
        return lambda underlying_price: calc_put_value(
            underlying_price=underlying_price,
            strike_price=strike_price,
            multiplier=multiplier,
        )
