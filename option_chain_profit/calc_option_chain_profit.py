from ib_insync import IB, Option, Contract
import pandas as pd
import numpy as np

def calc_profit(
    ask: float,
    strike: float,
    multiplier: int,
    future_price: float,
    right: str,
) -> float:
    if right == "P" or right == "PUT":
        return ((-1.0 * ask) + (strike - future_price)) * multiplier
    else:
        return ((-1.0 * ask) + (future_price - strike)) * multiplier

def calc_option_chain_profit(
    ib: IB,
    qualified_contract: Contract,
    expirations: str,
    future_price: float,
    use_delayed_data=True,
    strike_max=None,
    strike_min=None,
    rights=["P", "C"],
) -> pd.DataFrame:
    """
    TODO: Write documentation

    strike_max and strike_min default to 10% of the current value, or the future_price
    """
    if use_delayed_data:
        ib.reqMarketDataType(3)
    [ticker] = ib.reqTickers(qualified_contract)
    current_price = ticker.marketPrice()

    chains = ib.reqSecDefOptParams(qualified_contract.symbol, '', qualified_contract.secType, qualified_contract.conId)
    chain = next(c for c in chains
                 if c.tradingClass == qualified_contract.symbol
                 and c.exchange == qualified_contract.exchange)

    strike_max = strike_max or max(future_price, (current_price * 1.10))
    strike_min = strike_min or min(future_price, (current_price * 0.90))
    strikes = [strike for strike in chain.strikes
               if strike_min < strike < strike_max]
               #and strike % 5 == 0]

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

    contract_months = [ticker.contract.lastTradeDateOrContractMonth for ticker in tickers]
    strike_prices = [ticker.contract.strike for ticker in tickers]
    rights = [ticker.contract.right for ticker in tickers]
    cost_per_contracts = [(ticker.ask * int(ticker.contract.multiplier)) for ticker in tickers]
    profit_per_contracts = [calc_profit(ticker.ask, ticker.contract.strike, int(ticker.contract.multiplier), future_price, ticker.contract.right) for ticker in tickers]
    profit_per_cost_dollar = np.asarray(profit_per_contracts) / np.asarray(cost_per_contracts)

    d = {
        "ContractMonth": contract_months,
        "StrikePrice": strike_prices,
        "Right": rights,
        "CostPerContract": cost_per_contracts,
        "ProfitsPerContract": profit_per_contracts,
        "ProfitPerCostDollar": profit_per_cost_dollar,
        }
    df = pd.DataFrame(data=d)

    return df
