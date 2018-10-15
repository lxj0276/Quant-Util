from quantlab.feature import *
from quantlab.feature.ops import *
from numpy.core.umath import exp, log1p, sqrt
from numpy.core.multiarray import array as np_array
from numpy.core.fromnumeric import sum as np_sum
from numpy.lib.nanfunctions import nanmean, nanstd, nansum
import pandas as pd


class Halflife_Std_Daily(NonPersistentFeature):
    description = '过去22天的收益率按时间半衰加权波动'
    formula = 'Std（过去22天收益率*半衰权重）'
    granularity = 'day'
    
    def _create_feature(self, instrument_id, time_range):
        def Halflife_std(x):
            halflife = np_array([1/2**((len(x)-i-1)/66) for i in range(len(x))])
            halflife = halflife*len(x)/np_sum(halflife)
            temp_x = pd.Series(x,index=halflife).map(lambda y: (y-nanmean(x))**2)
            return sqrt((temp_x * temp_x.index).sum()/len(x))
        change = ChangeRate_Daily()
        halflife_std = Rolling(change, 22, Halflife_std)
        return halflife_std.load(instrument_id, time_range)       
