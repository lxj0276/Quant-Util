from feature.ops import *


def BBI(close, m=3, n=6, k=12, l=24):
    bbi = Add(Add(Add(MA(close, m), MA(close, n)), MA(close, k)), MA(close, l))
    return bbi
