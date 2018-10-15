from quantlab.feature import *
from .KDJ import KDJ


class KDJJ_Daily(PersistentFeature):

    description = 'J of KDJ'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        close = Close_Daily()
        high = High_Daily()
        low = Low_Daily()
        _,_,J = KDJ(close, high, low)
        return J.load(instrument_id, time_range)
