from quantlab.feature.ops import *


def VR(close, volume, window):
    change = Sub(close, Shift(close, 1))
    upindex = Map(change, lambda x: 1.0 if x>0 else 0.0)
    downindex = Map(change, lambda x: 1.0 if x<0 else 0.0)
    AVS = Rolling(Mul(volume, upindex), window, sum)
    BVS = Rolling(Mul(volume, downindex), window, sum)
    VR = Div(AVS, BVS)
    return VR
