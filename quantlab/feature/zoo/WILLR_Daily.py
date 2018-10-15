from quantlab.feature import *
from .WILLR import WILLR


class WILLR_Daily(PersistentFeature):

    description = '多空指标，是一个负数，接近0为多头市场，接近-1为空头市场'
    formula = '-(过去14天最高-今日收盘)/(过去14天最高-过去14天最低)'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        close = Close_Daily()
        high = High_Daily()
        low = Low_Daily()
        w = WILLR(close, high, low, window=14)
        return w.load(instrument_id, time_range)
