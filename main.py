import time
import ccxt
import pandas as pd
import numpy as np

#This are the inputs for our study. You can change them if you want to have
#Different results.
market = "BTC/USDT"
ema_lenght = 13
williams_lenght = 21
ema_list = [0] * williams_lenght
williams_list = [0] * ema_lenght

#We add the counters of our recolected results. We also add the position open/close and the trend information.
profit = 0
profit_count = 0
loss = 0
loss_count = 0
calculate = int(0)
leverage = 3
position = False
trend = False
last_price = float(0)
close_position = float(0)

#We add the EMA calculator.
def ema(values, ema_length):
    alpha = 2 / (ema_length + 1)
    ema = np.zeros(len(values))
    ema[0] = values[0]
    for i in range(1, len(values)):
        ema[i] = alpha * values[i] + (1 - alpha) * ema[i-1]
    return ema

#We make the non-stop loop in order to keep our study working until we stop it.
while True:

    #We are using the data from Binance thru the CCXT library. If you want to
    #Make this into one strategy, you can change the API into yours.
    exchange = ccxt.binance({"Public Key": "XXXXX", "Secret Key": "XXXXX"})
    prices = exchange.fetch_ohlcv(symbol=market, timeframe="1m", limit=williams_lenght)

    closing_prices = [candle[4] for candle in prices]
    closing = pd.DataFrame(closing_prices)

    highest_prices = [candle[2] for candle in prices]
    highest = pd.DataFrame(highest_prices)

    lowest_prices = [candle[3] for candle in prices]
    lowest = pd.DataFrame(lowest_prices)

    #Now that we got the data, we can start taking the variables of the Williams %R
    highest_high = highest.max()
    highest_high = float(highest_high)
    lowest_low = lowest.min()
    lowest_low = float(lowest_low)
    last_close = closing_prices[0]

    #We calculate the Williams %R and we save it in one dataframe.
    williams = ((last_close - highest_high) / (highest_high - lowest_low)) * 100
    williams_list[1:] = williams_list[:-1]
    williams_list[0] = williams
    w = pd.DataFrame(williams_list)

    #Now we calculate the EMA of the Williams %R and we add it to our list.
    ema_list[1:] = ema_list[:-1]
    ema_list[0] = ema(williams_list, ema_lenght)

    #Now that we got all our data, we start with our study.
    #We calculate the trend of our EMA by looking for the direction of it.
    #If the EMA from the last data its less than our current EMA, then the trend its positive.
    #If not, then the trend its negative.
    if (ema_list[0] > ema_list[1]).all():
        trend = True

    else:
        trend = False

    #In order to open one position, we need to have:
    #The crossover between the Williams %R, no open positions and one positive trend.
    if williams == ema and position is False and trend is True:
        last_price = closing[0]
        position = True

    #Now, in our next close we end our position.
    if last_price == closing.iloc[0,0] and position is True:
        close_position = last_price
        calculate = (closing[0] - close_position) * leverage
        position = False

    #Now we calculate our profit or our loss and we add it to our recolected results.
    if calculate > 0:
        profit = profit + calculate
        profit_count += 1

    if calculate < 0:
        loss = loss + calculate
        loss_count += 1

    #We return the result of our study every iteration.
    print(f"Total Profit: {profit} over {profit_count} profits deals")
    print(f"Total Loss: {loss} over {loss_count} loss deals")

    #We add the time of waiting for every iteration.
    time.sleep(60)
