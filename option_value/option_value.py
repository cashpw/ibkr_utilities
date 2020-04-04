from ibkr_utilities.util.is_call import is_call

def build_option_value_fn(strike_price: float, right: str, multiplier=100):
    if is_call(right):
        return lambda underlying_price: 0 if underlying_price <= strike_price else ((underlying_price - strike_price) * multiplier)
    else:
        return lambda underlying_price: 0 if underlying_price >= strike_price else ((strike_price - underlying_price) * multiplier)
