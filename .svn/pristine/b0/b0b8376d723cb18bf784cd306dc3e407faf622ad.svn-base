from quantlab.feature.ops import *


def OBV(close, high, low, volume):
    up = Sub(close, low)
    down = Sub(high, close)
    maxdiv = Sub(high, low)
    return Mul(Div(Sub(up, down), maxdiv), volume)
