from decimal import Decimal
from option_value import build_option_value_fn

PUT = "PUT"
CALL = "CALL"

def test_in_the_money_put():
    fn = build_option_value_fn(strike_price=Decimal(2.0), right=PUT)

    assert fn(underlying_price=Decimal(1.0)) == 100.0

def test_out_of_the_money_put():
    fn = build_option_value_fn(strike_price=Decimal(1.0), right=PUT)

    assert fn(underlying_price=Decimal(2.0)) == 0

def test_at_the_money_put():
    fn = build_option_value_fn(strike_price=Decimal(1.0), right=PUT)

    assert fn(underlying_price=Decimal(1.0)) == 0

def test_in_the_money_call():
    fn = build_option_value_fn(strike_price=Decimal(1.0), right=CALL)

    assert fn(underlying_price=Decimal(2.0)) == 100.0

def test_out_of_the_money_call():
    fn = build_option_value_fn(strike_price=Decimal(2.0), right=CALL)

    assert fn(underlying_price=Decimal(1.0)) == 0

def test_at_the_money_call():
    fn = build_option_value_fn(strike_price=Decimal(1.0), right=CALL)

    assert fn(underlying_price=Decimal(1.0)) == 0
