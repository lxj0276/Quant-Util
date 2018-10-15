from quantlab.feature.ops import *
from scipy.stats import linregress


def Beta(change, id, window):
    benchmark = Mask(change, id)
    beta = Multi_rolling([benchmark, change], window, lambda x:linregress(x).slope)
    return beta
