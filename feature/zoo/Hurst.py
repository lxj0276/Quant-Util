"""
	Hurst exponent and RS-analysis
	https://en.wikipedia.org/wiki/Hurst_exponent
	https://en.wikipedia.org/wiki/Rescaled_range
"""

__version__ = '0.0.1'

import math

import numpy as np
from feature.ops import *


# def to_inc(x):
#     pct= list(map(lambda x1, x2: float(x2) - x1, x, x[1:]))
#     return pct

def to_inc(x):
    return x[1:] - x[:-1]


# def to_pct(x):
#     pct = map(lambda x1, x2: float(x2) / x1 - 1., x, x[1:])
#     return list(pct)

def to_pct(x):
    return x[1:] / x[:-1]


"""
	get_RS - get rescaled range from time-series of values (i.e. stock prices)
"""


def get_RS(series):
    incs = to_inc(series)

    R = math.fabs(max(series) - min(series))  # range
    S = incs.std()  # standard deviation
    return R / S


"""
	computeCH - compute c and H according to Hurst equiation
"""


def compute_Hc(series):
    series = series[~np.isnan(series)]


    window_sizes = list(map(
        lambda x: int(10 ** x),
        np.arange(1., math.log10(len(series) - 1), 0.25)))
    window_sizes.append(len(series))

    RS = []
    for w in window_sizes:
        rs = []
        for start in range(0, len(series), w):
            if (start + w) > len(series):
                break
            rs.append(get_RS(series[start:start + w]))
        RS.append(np.average(rs))

    A = np.vstack([np.log10(window_sizes), np.ones(len(RS))]).T
    H, c = np.linalg.lstsq(A, np.log10(RS))[0]
    c = 10 ** c
    return H, c


def herst_with_importance(series):
    n_repeat = 1000
    series_len = len(series)
    log_return = np.empty(series_len - 1)
    for i in range(log_return.shape[0]):
        log_return[i] = series[i + 1] / series[i] - 1

    H_series, c_series = compute_Hc(series)

    Hs = np.empty(n_repeat)
    for i in range(n_repeat):
        prices = np.empty(series_len)
        prices[0] = 100
        random_changes = np.random.randn(series_len - 1) * log_return.std()
        for j in range(1, len(prices)):
            prices[j] = prices[j - 1] * (1. + random_changes[j - 1] / 100)
        H, c = compute_Hc(prices)
        Hs[i] = H
    upper = (Hs > H_series).sum() / n_repeat
    return H_series, max(upper, 1 - upper), Hs.std()


def hurst(series):
    H_series, c_series = compute_Hc(series)
    return H_series


class Hurst(Rolling):
    def __init__(self, feature, window):
        super(Hurst, self).__init__(feature, window, hurst)


if __name__ == '__main__':
    prices = [100.]
    series = np.random.randn(399) + 0.4
    for pct_change in series:
        prices.append(prices[-1] * (1. + pct_change / 100))

    for i in range(1000):
        H, c = compute_Hc(np.array(prices))

    import pandas as  pd

    df = pd.DataFrame(np.random.randn(300, 3) / 10 + 1, columns=list('ABC'))
    df.rolling(window=100).apply()




