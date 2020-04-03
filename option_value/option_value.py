def build_option_value_fn(strike_price: float, right: str, multiplier=100):
    if right == 'P' or right == 'PUT':
        return lambda price: 0 if price >= strike_price else ((strike_price - price) * multiplier)
    else:
        return lambda price: 0 if price <= strike_price else ((price - strike_price) * multiplier)
