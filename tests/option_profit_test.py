from decimal import Decimal
from option_profit import build_option_profit_fn

PUT = "PUT"
CALL = "CALL"

def test_put_loss():
    fn = build_option_profit_fn(purchase_price=Decimal(0.2), strike_price=Decimal(2.0), right=PUT)

    assert fn(underlying_price=Decimal(2.0)) == -20.0

def test_put_neutral():
    fn = build_option_profit_fn(purchase_price=Decimal(0.2), strike_price=Decimal(2.0), right=PUT)

    assert fn(underlying_price=Decimal(1.80)) == 0

def test_put_gain():
    fn = build_option_profit_fn(purchase_price=Decimal(0.2), strike_price=Decimal(2.0), right=PUT)

    assert fn(underlying_price=Decimal(1.0)) == 80

def test_call_loss():
    fn = build_option_profit_fn(purchase_price=Decimal(0.2), strike_price=Decimal(1.0), right=CALL)

    assert fn(underlying_price=Decimal(1.0)) == -20.0

def test_call_neutral():
    fn = build_option_profit_fn(purchase_price=Decimal(0.2), strike_price=Decimal(1.0), right=CALL)

    assert fn(underlying_price=Decimal(1.20)) == 0

def test_call_gain():
    fn = build_option_profit_fn(purchase_price=Decimal(0.2), strike_price=Decimal(1.0), right=CALL)

    assert fn(underlying_price=Decimal(2.0)) == 80
