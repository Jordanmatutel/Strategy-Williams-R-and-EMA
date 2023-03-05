import time
import ccxt
import pandas as pd
import calculator as clc

leverage = 3
market = "BTC/USDT"
ema_lenght = 13
williams_lenght = 21

while True:
    # We are using the data from Binance thru the CCXT library. If you want to
    # Make this into one strategy, you can change the API into yours.
    exchange = ccxt.binance({"Public Key": "XXXXX", "Secret Key": "XXXXX"})
    prices = exchange.fetch_ohlcv(symbol=market, timeframe="1m", limit=williams_lenght)

    highest_prices = [candle[2] for candle in prices]
    highest = pd.DataFrame(highest_prices)

    lowest_prices = [candle[3] for candle in prices]
    lowest = pd.DataFrame(lowest_prices)

    closing_prices = [candle[4] for candle in prices]
    closing = pd.DataFrame(closing_prices)

    # Now we calculate the EMA of the Williams %R and we add it to our list.
    williams_list = clc.williamsCalculator(highest, lowest, closing)
    ema = williams_list[0].ewm(alpha=1, adjust=False).mean()
    trend = clc.trendDetector(closing_prices)  # Use the SMA to verify the trend
    williams = williams_list[0]
    williams = williams[0]     # Take the last Williams %R value
    signal = clc.Signal(williams, ema, trend)

    position = False
    entry = 0
    close = 0
    profitSum = (entry - close) * leverage

    if signal and position == False:
        entry = closing_prices[0]
        position = True

    if position and not signal:
        close = closing_prices[0]
        position = False

    print("The total of profit:", profitSum)

    time.sleep(60)
