from decimal import Decimal, ROUND_HALF_DOWN
from option_value import build_option_value_fn

def calc_profit(value: Decimal, purchase_price: Decimal, multiplier: int) -> Decimal:
    print(f"value: {value}")
    value = Decimal(value - (purchase_price * multiplier))
    return Decimal(value.quantize(Decimal('.01'), rounding=ROUND_HALF_DOWN))

def build_option_profit_fn(purchase_price: Decimal, strike_price: Decimal, right: str, multiplier=100):
    value_fn = build_option_value_fn(strike_price=strike_price, right=right, multiplier=multiplier)
    return lambda underlying_price: calc_profit(
        value=value_fn(underlying_price),
        purchase_price=purchase_price,
        multiplier=multiplier,
    )
