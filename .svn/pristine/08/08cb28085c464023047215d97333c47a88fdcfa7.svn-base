from quantlab.feature import *
from .RSI import RSI


class RSI6_Daily(PersistentFeature):

    description = '多空指标，短周期RSI在长周期RSI之上时为多头市场，反之为空头市场'
    formula = 'upmean 是过去N天上涨日涨幅之和，downmean是过去N天下跌日跌幅之和，RSI=upmean/(upmean+downmean)'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):

        close = Close_Daily()
        rsi = RSI(close, 6)
        return rsi.load(instrument_id, time_range)
