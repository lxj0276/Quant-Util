from quantlab.feature.ops import *
from numpy.lib.nanfunctions import nanmean, nanstd


def Sharpe(change, window=40):
    '''
    Sharpe = 收益率均值/方差
    '''
    def get_sharpe(x):
        mean = nanmean(x)
        std = nanstd(x)
        return mean/std
    return Rolling(change, window, get_sharpe)
