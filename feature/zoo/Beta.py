from scipy.stats import linregress

from feature.ops import *


def Beta(change, id, window):
    benchmark = Mask(change, id)
    beta = Multi_rolling([benchmark, change], window, lambda x: linregress(x).slope)
    return beta
