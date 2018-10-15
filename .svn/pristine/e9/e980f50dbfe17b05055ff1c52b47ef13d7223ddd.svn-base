from quantlab.feature import NonPersistentFeature
from quantlab import feature
from quantlab.feature.ops import *
from quantlab.feature import *

class Inv_Halflife_Std_Daily(NonPersistentFeature):
    description = '过去22天的收益率按时间半衰加权波动的倒数'
    formula = '1/Std（过去22天收益率*半衰权重）'
    granularity = 'day'
    
    def _create_feature(self, instrument_id, time_range):
        std=Div(1,Halflife_Std_Daily())
        return std.load(instrument_id,time_range)