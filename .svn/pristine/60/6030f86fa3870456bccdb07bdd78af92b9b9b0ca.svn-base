from feature.ops import *


def MFI(close, high, low, money, window=14):
    TP = Map(Add(Add(close, high), low), lambda x: x / 3)
    TPchange = Sub(TP, Shift(TP, 1))
    PMFindex = Map(TPchange, lambda x: 1.0 if x > 0 else 0)
    NMFindex = Map(TPchange, lambda x: 1.0 if x < 0 else 0)
    PMF = Rolling(Mul(money, PMFindex), window, sum)
    NMF = Rolling(Mul(money, NMFindex), window, sum)
    MFR = Div(PMF, NMF)
    mfi = Map(MFR, lambda x: 100 - 100 / (1 + x))
    return mfi
