from quantlab.feature import *
from .VR import VR


class VR24_Daily(PersistentFeature):

    description = '多空指标，综合考虑股价变化与交易量，VR值大对应多头市场，反之为空头市场'
    formula = 'AVS:24日上涨日成交量之和，BVS:24日下跌日成交量之和，CVS:24日价格不变日成交量之和。VR=(AVS+0.5CVS)/(BVS+0.5CVS)'
    # 我们不考虑CVS，因为CVS很难出现
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        close = Close_Daily()
        volume = Vol_Daily()
        VR24 = VR(close, volume, 24)
        return VR24.load(instrument_id, time_range)
