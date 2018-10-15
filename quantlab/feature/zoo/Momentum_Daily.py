from quantlab.feature import *
from quantlab.feature.ops import *
from numpy.core.umath import exp, log1p, sqrt
from numpy.core.multiarray import array as np_array
from numpy.core.fromnumeric import sum as np_sum
from numpy.lib.nanfunctions import nanmean, nanstd, nansum


class Momentum_Daily(PersistentFeature):
    description = '动量因子'
    formula = '过去22天的累计年化收益率'
    granularity = 'day'
    
    def _create_feature(self, instrument_id, time_range):
        change = ChangeRate_Daily()
        momentum = Rolling(change, 22, lambda x: exp(nansum((log1p(x))))**(252/22)-1)
        return momentum.load(instrument_id, time_range)
