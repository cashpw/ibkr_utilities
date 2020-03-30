from calc_option_chain_profit import calc_option_chain_profit
from ib_insync import IB, Stock

ib = IB()
ib.connect()

spy = Stock("SPY", "SMART", "USD")
ib.reqMarketDataType(3)
ib.qualifyContracts(spy)

df = calc_option_chain_profit(ib, spy, ["20200417"], 220.0)
df = df.sort_values(by=["ProfitPerCostDollar"], ascending=False)

print("\n\n")
print(df.head(10))

ib.disconnect()
