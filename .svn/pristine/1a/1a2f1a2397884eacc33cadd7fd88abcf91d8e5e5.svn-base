from quantlab.feature import *
from quantlab.feature.ops import *
from numpy.core.multiarray import array as np_array
from numpy.core.fromnumeric import sum as np_sum
from numpy.lib.nanfunctions import nanmean, nanstd, nansum


class Halflife_Kurtosis_Daily(NonPersistentFeature):
    description = '半衰加权的个股历史22日收益率的峰度'
    formula = ' Kurtosis = E[(x-Ex)^4/Var(x)^2]-3 '
    granularity = 'day'
    
    def _create_feature(self, instrument_id, time_range):
        def get_kurtosis(x):
            halflife = np_array([1/2**((len(x)-i-1)/66) for i in range(len(x))])
            halflife = halflife*len(x)/np_sum(halflife)
            neu_x=((x-nanmean(x))/nanstd(x))**4
            return nansum(neu_x*halflife)/len(x)-3
            
        kurtosis=Rolling(ChangeRate_Daily(),22,get_kurtosis)
        return kurtosis.load(instrument_id,time_range)
