from quantlab.feature import *
from quantlab.feature.ops import *
from numpy.core.multiarray import array as np_array
from numpy.core.fromnumeric import sum as np_sum
import pandas as pd


class Halflife_CVAR_Daily(PersistentFeature):
    description = 'CVAR衡量过去一段时间的期望极端亏损，考虑到极端亏损对现在的影响应当是随时间不断衰减的，Halflife_CVAR是按照半衰的思想加权的期望极端亏损'
    formula = 'Halflife_CVAR = 按日期半衰的CVAR'
    granularity = 'day'
    
    def _create_feature(self, instrument_id, time_range):
        def Halflife_CVAR(x,n=3):
            halflife = np_array([1/2**((len(x)-i-1)/66) for i in range(len(x))])
            halflife = halflife*len(x)/np_sum(halflife)
            temp_x = pd.Series(x,index=halflife).sort_values(ascending=True).head(n)
            return (temp_x * temp_x.index).sum()

        change = ChangeRate_Daily()
        halflife_cvar=Rolling(change,22, Halflife_CVAR)
        return halflife_cvar.load(instrument_id,time_range)
