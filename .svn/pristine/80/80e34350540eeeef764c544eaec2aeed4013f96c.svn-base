from quantlab.feature import *
from .KDJ import KDJ


class KDJK_Daily(PersistentFeature):

    description = 'K of KDJ'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        close = Close_Daily()
        high = High_Daily()
        low = Low_Daily()
        K,_,_ = KDJ(close, high, low)
        return K.load(instrument_id, time_range)
