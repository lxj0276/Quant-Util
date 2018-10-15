from quantlab.feature.ops import *


def DEA(close, m=12, n=26, k=9):
    diff = Sub(EMA(close, m), EMA(close, n))
    dea = EMA(diff, k)
    return dea
