from feature.ops import *


def PSY(close, window):
    change = Sub(close, Shift(close, 1))
    upday_index = Map(change, lambda x: 1.0 if x > 0 else 0)
    psy = MA(upday_index, window)
    return psy
