from numpy.core.fromnumeric import argmax, argmin

from feature.ops import *


def Aroon(price, down, window=25):
    def get_aroon(x):
        if down:
            target = argmin(x)
        else:
            target = argmax(x)
        return (target + 1) / len(x) * 100

    aroon = Rolling(price, window, get_aroon)
    return aroon
