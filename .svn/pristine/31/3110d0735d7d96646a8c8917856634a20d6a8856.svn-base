from quantlab.feature.ops import *

def MACD(close, m=12, n=26, k=9):
    diff = Sub(EMA(close, m), EMA(close, n))
    dea = EMA(diff, k)
    macd = Scale(Sub(diff, dea),2)
    return macd