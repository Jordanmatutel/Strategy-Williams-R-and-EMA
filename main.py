import time
import ccxt
import pandas as pd


def williamsCalculator(highest, lowest, closing_prices):
    williams_list = [0] * len(highest)
    highest_high = highest.max()
    highest_high = float(highest_high)
    lowest_low = lowest.min()
    lowest_low = float(lowest_low)
    last_close = closing_prices[0]
    #We calculate the Williams %R and we save it in one dataframe.
    williams = ((last_close - highest_high) / (highest_high - lowest_low)) * 100
    williams_list[1:] = williams_list[:-1]
    williams_list[0] = williams
    return williams_list

def trendDetector(closing_prices):
    if closing_prices[0] > closing_prices[1]:
        trend = True
    else:
        trend = False
    return trend

def Signal(williams, EMA, trend):
    signal = williams[0] - EMA[0]
    if signal.between(-0.10, 0.10).all():
        if trend:
            buy = True
    else:
        buy = False
    return buy

leverage = 3
market = "BTC/USDT"
ema_lenght = 13
williams_lenght = 21

while True:
    # We are using the data from Binance thru the CCXT library. If you want to
    # Make this into one strategy, you can change the API into yours.
    exchange = ccxt.binance({"Public Key": "XXXXX", "Secret Key": "XXXXX"})
    prices = exchange.fetch_ohlcv(symbol=market, timeframe="1m", limit=williams_lenght)

    closing_prices = [candle[4] for candle in prices]
    closing = pd.DataFrame(closing_prices)

    highest_prices = [candle[2] for candle in prices]
    highest = pd.DataFrame(highest_prices)

    lowest_prices = [candle[3] for candle in prices]
    lowest = pd.DataFrame(lowest_prices)

    #Now we calculate the EMA of the Williams %R and we add it to our list.
    williams_list = williamsCalculator(highest, lowest, closing)
    ema = williams_list[0].ewm(alpha=1, adjust=False).mean()
    trend = trendDetector(closing_prices)
    signal = Signal(williams_list, ema, trend)

    position = False
    entryCall = 0
    closePrice = 0
    profitSum = (entryCall - closePrice) * leverage

    if Signal and position:
        lastCall = closing_prices[0]

    if position and not Signal:
        closePrice = closing_prices[0]
        position = False

    print("The total of profit:", profitSum)

    time.sleep(60)