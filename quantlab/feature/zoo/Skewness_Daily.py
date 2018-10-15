from quantlab.feature import *
from quantlab.feature.ops import *
from numpy.core.umath import exp, log1p, sqrt
from numpy.core.multiarray import array as np_array
from numpy.core.fromnumeric import sum as np_sum
from numpy.lib.nanfunctions import nanmean, nanstd, nansum


class Skewness_Daily(NonPersistentFeature):
    description = '个股历史22日收益率的偏度'
    formula = 'Skewness = E[(R)^3], R=(r-mu)/sigma '
    granularity = 'day'
    
    def _create_feature(self, instrument_id, time_range):
        def get_skewness(x):
            neu_x=((x-nanmean(x))/nanstd(x))**3
            return nanmean(neu_x)
            
        skewness = Rolling(ChangeRate_Daily(), 22, get_skewness)
        return skewness.load(instrument_id, time_range)
