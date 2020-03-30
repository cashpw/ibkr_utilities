from ib_insync import IB, Option, Contract
import pandas as pd
import numpy as np

def calcProfit(
    ask: float,
    strike: float,
    multiplier: int,
    futurePrice: float,
    right: str,
) -> float:
    if right == "P" or right == "PUT":
        return ((-1.0 * ask) + (strike - futurePrice)) * multiplier
    else:
        return ((-1.0 * ask) + (futurePrice - strike)) * multiplier

def calcOptionChainProfit(
    ib: IB,
    qualifiedContract: Contract,
    expirations: str,
    futurePrice: float,
    useDelayedData=True,
    strikeMax=None,
    strikeMin=None,
    rights=["P", "C"],
) -> pd.DataFrame:
    """
    TODO
    strikeMax and strikeMin default to 10% of the current value, or the futurePrice
    """
    if useDelayedData:
        ib.reqMarketDataType(3)
    [ticker] = ib.reqTickers(qualifiedContract)
    currentValue = ticker.marketPrice()

    chains = ib.reqSecDefOptParams(qualifiedContract.symbol, '', qualifiedContract.secType, qualifiedContract.conId)
    chain = next(c for c in chains
                 if c.tradingClass == qualifiedContract.symbol
                 and c.exchange == qualifiedContract.exchange)

    strikeMax = strikeMax or max(futurePrice, (currentValue * 1.10))
    strikeMin = strikeMin or min(futurePrice, (currentValue * 0.90))
    strikes = [strike for strike in chain.strikes
               if strikeMin < strike < strikeMax]
               #and strike % 5 == 0]

    contracts = [Option(qualifiedContract.symbol, expiration, strike, right, qualifiedContract.exchange, tradingClass=qualifiedContract.symbol)
            for right in rights
            for expiration in expirations
            for strike in strikes]

    if useDelayedData:
        ib.reqMarketDataType(3)
    ib.qualifyContracts(*contracts)

    contracts = [contract for contract in contracts if contract.multiplier]

    if useDelayedData:
        ib.reqMarketDataType(3)
    tickers = ib.reqTickers(*contracts)

    contractMonths = [ticker.contract.lastTradeDateOrContractMonth for ticker in tickers]
    strikePrices = [ticker.contract.strike for ticker in tickers]
    rights = [ticker.contract.right for ticker in tickers]
    costPerContracts = [(ticker.ask * int(ticker.contract.multiplier)) for ticker in tickers]
    profitPerContracts = [calcProfit(ticker.ask, ticker.contract.strike, int(ticker.contract.multiplier), futurePrice, ticker.contract.right) for ticker in tickers]
    profitPerCostDollar = np.asarray(profitPerContracts) / np.asarray(costPerContracts)

    d = {
        "ContractMonth": contractMonths,
        "StrikePrice": strikePrices,
        "Right": rights,
        "CostPerContract": costPerContracts,
        "ProfitsPerContract": profitPerContracts,
        "ProfitPerCostDollar": profitPerCostDollar,
        }
    df = pd.DataFrame(data=d)

    return df
