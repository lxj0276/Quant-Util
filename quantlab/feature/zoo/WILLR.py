from quantlab.feature.ops import *

def WILLR(close, high, low, window=14):
    high = Rolling(high, window, max)
    low = Rolling(low, window, min)
    return Div(Sub(high, close), Sub(high, low))