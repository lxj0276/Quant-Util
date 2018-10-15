from feature.ops import *
from .TR import TR


def ADX(close, high, low, n=14, m=14):
    p_DM = Map(Sub(high, Shift(high, 1)), lambda x: x if x > 0 else 0)
    n_DM = Map(Sub(Shift(low, 1), low), lambda x: x if x > 0 else 0)
    p_index = Map(Sub(p_DM, n_DM), lambda x: 1.0 if x > 0 else 0)
    n_index = Map(Sub(n_DM, p_DM), lambda x: 1.0 if x > 0 else 0)
    p_DM14 = MA(Mul(p_DM, p_index), n)
    n_DM14 = MA(Mul(n_DM, n_index), n)
    tr = TR(close, high, low)
    tr14 = MA(tr, n)
    p_DI = Div(p_DM14, tr14)
    n_DI = Div(n_DM14, tr14)
    DX = Map(Div(Sub(p_DI, n_DI), Add(p_DI, n_DI)), abs)
    ADX = EMA(DX, m)
    return ADX
