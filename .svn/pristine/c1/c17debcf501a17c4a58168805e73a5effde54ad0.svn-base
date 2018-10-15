from feature.ops import *


def TR(close, high, low):
    temp1 = Map(Sub(high, low), abs)
    temp2 = Map(Sub(Shift(close, 1), high), abs)
    temp3 = Map(Sub(Shift(close, 1), low), abs)
    TR = Multi_rolling([temp1, temp2, temp3], 1, lambda x: x.squeeze().max())
    return TR
