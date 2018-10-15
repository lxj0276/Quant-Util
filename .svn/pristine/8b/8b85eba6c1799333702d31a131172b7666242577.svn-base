from quantlab.feature import *
from quantlab.feature.ops import *
from numpy.core.umath import exp, log1p
from numpy.core.multiarray import array as np_array
from numpy.core.fromnumeric import sum as np_sum
from numpy.lib.nanfunctions import nanmean, nanstd, nansum
import pandas as pd


class Halflife_Momentum_Daily(NonPersistentFeature):
    description = '半衰动量因子'
    formula = '过去22天收益率按半衰加权的累计年化收益率'
    granularity = 'day'
    
    def _create_feature(self, instrument_id, time_range):
        change = ChangeRate_Daily()
        def halflife_momentum(x):
            halflife = np_array([1/2**((len(x)-i-1)/66) for i in range(len(x))])
            halflife = halflife*len(x)/np_sum(halflife)
            return exp(nansum((halflife*log1p(x))))**(252/22)-1
        Halflife_momentum_ = Rolling(change, 22, halflife_momentum)
        return Halflife_momentum_.load(instrument_id, time_range)
