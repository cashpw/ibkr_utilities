from option_value import build_option_value_fn

def build_option_profit_fn(purchase_price: float, strike_price: float, right: str):
    value_fn = build_option_value_fn(strike_price=strike_price, right=right)
    return lambda underlying_price: value_fn(underlying_price) - purchase_price
