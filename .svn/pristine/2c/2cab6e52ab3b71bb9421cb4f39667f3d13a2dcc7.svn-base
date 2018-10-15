from quantlab.feature import *
from .KDJ import KDJ


class KDJD_Daily(PersistentFeature):

    description = 'D of KDJ'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        close = Close_Daily()
        high = High_Daily()
        low = Low_Daily()
        _,D,_ = KDJ(close, high, low)
        return D.load(instrument_id, time_range)
