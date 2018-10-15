from feature.ops import *


def EMV(high, low, money, window):
    PRsub = Add(high, low)
    PR = Sub(PRsub, Shift(PRsub, 1))
    PV = Div(money, Sub(high, low))
    return Sum(Div(Div(PR, PV), 2), window)
