from feature.ops import *


def BOLL(close, down, window=20):
    std2 = Map(Vola(close, window), lambda x: x * 2)
    ma = MA(close, window)
    if down:
        bool = Sub(ma, std2)
    else:
        bool = Add(ma, std2)
    return bool
