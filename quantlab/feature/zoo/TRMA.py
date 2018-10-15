from quantlab.feature.ops import *
from .TRIX import TRIX


def TRMA(close, n=12, m=20):
    trix = TRIX(close, n)
    trma = MA(trix, m)
    return trma
