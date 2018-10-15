from quantlab.feature.ops import *


def TRIX(close, window=12):
    TR = EMA(EMA(EMA(close, window),window),window)
    TRIX = Map(Div(TR, Shift(TR, 1)), lambda x:(x-1)*100)
    return TRIX
