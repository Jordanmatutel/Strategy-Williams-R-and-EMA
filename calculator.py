import numpy as np


def williamsCalculator(highest, lowest, closing_prices):
    williams_list = [0] * len(highest)
    highest_high = highest.max()
    highest_high = float(highest_high)
    lowest_low = lowest.min()
    lowest_low = float(lowest_low)
    last_close = closing_prices[0]
    # We calculate the Williams %R and we save it in one dataframe.
    williams = ((last_close - highest_high) / (highest_high - lowest_low)) * 100
    williams_list[1:] = williams_list[:-1]
    williams_list[0] = williams
    return williams_list


def trendDetector(closing_prices):
    nparray = np.array(closing_prices)
    sma10 = np.mean(nparray[-10])
    sma20 = np.mean(nparray[-20])
    if sma10 > sma20:
        f = True
    elif sma10 < sma20:
        f = False
    return f


def Signal(williams, EMA, trend):
    signal = williams - EMA[0]
    if signal <= 0.10 and signal >=  0.10:
        if trend:
            buy = True
    else:
        buy = False
    return buy
