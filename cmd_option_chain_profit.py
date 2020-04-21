from get_option_chain import get_option_chain
from ib_insync import IB, Stock, Index
from typing import List
import argparse
import pandas as pd

def calc_option_contract_profit(
    asks: List[float],
    strikes: List[float],
    multipliers: List[int],
    rights: List[str],
    future_price: float,
) -> List[float]:
    right_is_call = rights.apply(lambda right: 1 if right == "C" or right == "CALL" else -1)
    return ((-1.0 * asks) + (right_is_call * (future_price - strikes))) * multipliers

parser = argparse.ArgumentParser(description="Calculate option chain profits.")
parser.add_argument('symbol', type=str, help="The stock symbol (eg: GOOG) to use.")
parser.add_argument('-e', '--expirations', metavar="YYYYMMDD", type=str, nargs="+", help="Option expiration date(s).", required=True)
parser.add_argument('-f', '--future_prices', type=float, nargs="+", help="Future price(s) for computing profit.", required=True)
parser.add_argument('-m', '--strike_modulus', type=int, help="Modulus value for strike prices", required=False)
parser.add_argument('--contract_per_price', dest="contract_per_price", type=int, default=3)
args = parser.parse_args()

pd.set_option("display.max_rows", None)

ib = IB()
ib.connect()

contract = Stock(args.symbol, "SMART", "USD")
ib.reqMarketDataType(1)
ib.qualifyContracts(contract)
[ticker] = ib.reqTickers(contract)
current_price = ticker.marketPrice()

strike_min=min(current_price * 0.9, min(args.future_prices))
strike_max=max(current_price * 1.1, max(args.future_prices))
strike_modulus = args.strike_modulus or None
option_chain = get_option_chain(ib, contract, args.expirations, strike_min=strike_min, strike_max=strike_max, strike_modulus=strike_modulus)

for future_price in args.future_prices:
    df = option_chain.copy()
    print("\n\n")
    print(f"For: {contract.symbol} with future price of {future_price}")
    df["Price"] = df["Ask"] * df["Multiplier"]
    df["ProfitPerContract"] = calc_option_contract_profit(df["Ask"], df["Strike"], df["Multiplier"], df["Right"], future_price)
    df["ProfitPerDollar"] = df["ProfitPerContract"] / (df["Ask"] * df["Multiplier"])
    df.drop(columns=["Multiplier"])
    df = df.sort_values(by=["ProfitPerDollar"], ascending=False)

    by_expiration = df.groupby("Expiration")
    for expiration, frame in by_expiration:
        print(frame.head(args.contract_per_price), end="\n\n")

ib.disconnect()
