from feature.ops import *


def CMO(close, window):
    pct_change = Sub(Div(close, Shift(close, 1)), 1)
    su = Sum(Map(pct_change, lambda x: x if x >= 0 else 0), window)
    sd = Sum(Map(pct_change, lambda x: x if x < 0 else 0), window)
    return Mul(Div(Sub(su, sd), Add(su, sd)), 100)
