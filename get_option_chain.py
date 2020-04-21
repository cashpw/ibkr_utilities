from ib_insync import IB, Option, Contract
import pandas as pd

def get_option_chain(
    ib: IB,
    qualified_contract: Contract,
    expirations: str,
    use_delayed_data=False,
    strike_min=None,
    strike_max=None,
    strike_modulus=None,
    rights=["P", "C"],
) -> pd.DataFrame:
    """
    TODO: Write documentation
    """

    if use_delayed_data:
        ib.reqMarketDataType(3)
    [ticker] = ib.reqTickers(qualified_contract)
    current_price = ticker.marketPrice()
    strike_min = strike_min or current_price * 0.90
    strike_max = strike_max or current_price * 1.10

    chains = ib.reqSecDefOptParams(qualified_contract.symbol, '', qualified_contract.secType, qualified_contract.conId)
    chain = next(c for c in chains
                 if c.tradingClass == qualified_contract.symbol
                 and c.exchange == qualified_contract.exchange)
    if strike_modulus:
        strikes = [strike for strike in chain.strikes
                if strike_min < strike < strike_max
                and strike % strike_modulus == 0]
    else:
        strikes = [strike for strike in chain.strikes
                if strike_min < strike < strike_max]
    contracts = [Option(qualified_contract.symbol, expiration, strike, right, qualified_contract.exchange, tradingClass=qualified_contract.symbol)
            for right in rights
            for expiration in expirations
            for strike in strikes]

    if use_delayed_data:
        ib.reqMarketDataType(3)
    ib.qualifyContracts(*contracts)
    contracts = [contract for contract in contracts if contract.multiplier]

    if use_delayed_data:
        ib.reqMarketDataType(3)
    tickers = ib.reqTickers(*contracts)

    d = {
        "Expiration": [str(ticker.contract.lastTradeDateOrContractMonth) for ticker in tickers],
        "Strike": [ticker.contract.strike for ticker in tickers],
        "Right": [str(ticker.contract.right) for ticker in tickers],
        "Ask": [ticker.ask for ticker in tickers],
        "Multiplier": [int(ticker.contract.multiplier) for ticker in tickers],
        }
    return pd.DataFrame(data=d)
