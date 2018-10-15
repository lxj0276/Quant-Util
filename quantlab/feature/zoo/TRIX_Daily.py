from quantlab.feature import *
from .TRIX import TRIX


class TRIX_Daily(PersistentFeature):

    description = '中长线指标，有回归TRMA的趋势'
    formula = 'TR是close的三重EMA，TRIX=(TR/前日TR-1)*100'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        close = Close_Daily()
        TRIX12 = TRIX(close, 12)
        return TRIX12.load(instrument_id, time_range)
