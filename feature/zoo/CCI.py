from numpy import mean

from feature.ops import *


def CCI(close, high, low, window):
    TP = Map(Add(Add(close, low), high), lambda x: x / 3)
    maTP = MA(TP, window)
    D = Rolling(Map(Sub(TP, maTP), lambda x: abs(x)), window, lambda x: mean(abs(x - mean(x))))
    cci = Map(Div(Sub(TP, maTP), D), lambda x: x / 0.015)
    return cci
