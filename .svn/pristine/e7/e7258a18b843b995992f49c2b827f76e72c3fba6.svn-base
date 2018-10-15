from quantlab.feature import *
from quantlab.feature.ops import *


class AbnormalVolatility_Daily(NonPersistentFeature):
    description = '个股异动，描述个股波动性中市场市场无法解释的部分'
    formula = 'Abnormal Volatility = CAPM下回归残差的标准差（22天）'
    granularity = 'day'
    
    def _create_feature(self, instrument_id, time_range):
        from scipy.stats import linregress
        benchmark = Mask(ChangeRate_Daily(),'CN_IDX_SH000001')
        rate = ChangeRate_Daily()
        err_std = Multi_rolling([benchmark, rate], 22, lambda x: linregress(x).stderr)
        return err_std.load(instrument_id,time_range)
