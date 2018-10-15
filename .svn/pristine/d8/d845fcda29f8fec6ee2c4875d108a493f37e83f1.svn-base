from feature.ops import *


def KDJ(close, high, low, n=9, m=3):
    lowest = Rolling(low, n, min)
    highest = Rolling(high, n, max)
    RSV = Scale(Div(Sub(close, lowest), Sub(highest, lowest)), 100)
    K = MA(RSV, m)
    D = MA(K, m)
    J = Sub(Scale(K, 3), Scale(D, 2))
    return K, D, J
