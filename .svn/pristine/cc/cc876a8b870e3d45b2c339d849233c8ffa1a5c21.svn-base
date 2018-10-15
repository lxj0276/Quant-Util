from quantlab.feature.ops import *


def RSI(close, window=6):
    change = Sub(close, Shift(close, 1))
    up = Rolling(change, window, lambda x:sum(abs(x)+x)/2)
    down = Rolling(change, window, lambda x:sum(abs(x)-x)/2)
    RS = Div(up, down)
    RSI = Map(RS, lambda x:100-100/(1+x))
    return RSI
