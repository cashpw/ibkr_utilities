import unittest
from option_value import build_option_value_fn

PUT = "PUT"
CALL = "CALL"

class TestBuildOptionValueFn(unittest.TestCase):

    def test_in_the_money_put(self):
        fn = build_option_value_fn(strike_price=2.0, right=PUT)

        self.assertEqual(fn(price=1.0), 100.0)

    def test_out_of_the_money_put(self):
        fn = build_option_value_fn(strike_price=1.0, right=PUT)

        self.assertEqual(fn(price=2.0), 0)

    def test_at_the_money_put(self):
        fn = build_option_value_fn(strike_price=1.0, right=PUT)

        self.assertEqual(fn(price=1.0), 0)

    def test_in_the_money_call(self):
        fn = build_option_value_fn(strike_price=1.0, right=CALL)

        self.assertEqual(fn(price=2.0), 100.0)

    def test_out_of_the_money_call(self):
        fn = build_option_value_fn(strike_price=2.0, right=CALL)

        self.assertEqual(fn(price=1.0), 0)

    def test_at_the_money_call(self):
        fn = build_option_value_fn(strike_price=1.0, right=CALL)

        self.assertEqual(fn(price=1.0), 0)

if __name__ == '__main__':
    unittest.main()
