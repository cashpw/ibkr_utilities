from get_option_chain import get_option_chain
from ib_insync import IB, Stock
import pandas as pd
from typing import List

def calc_option_contract_profit(
    asks: List[float],
    strikes: List[float],
    multipliers: List[int],
    rights: List[str],
    future_price: float,
) -> List[float]:
    right_is_call = rights.apply(lambda right: 1 if right == "C" or right == "CALL" else -1)
    return ((-1.0 * asks) + (right_is_call * (future_price - strikes))) * multipliers

pd.set_option("display.max_rows", None)

ib = IB()
ib.connect()

contract = Stock("SPY", "SMART", "USD")
ib.reqMarketDataType(1)
ib.qualifyContracts(contract)

future_prices = [240.0, 230.0, 220.0]
expirations = ["20200417"]
option_chain = get_option_chain(ib, contract, expirations, strike_min=min(future_prices))

for future_price in future_prices:
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
        print(frame.head(15), end="\n\n")

ib.disconnect()
