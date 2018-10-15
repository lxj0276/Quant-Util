from scipy.stats import linregress

from feature.ops import *


def Alpha(change, id, window):
    benchmark = Mask(change, id)
    alpha = Multi_rolling([benchmark, change], window, lambda x: linregress(x).intercept)
    return alpha
