from feature.base import PersistentFeature
from feature.zoo.Close_Daily import Close_Daily
from feature.zoo.High_Daily import High_Daily
from feature.zoo.Low_Daily import Low_Daily

from .KDJ import KDJ


class KDJD_Daily(PersistentFeature):
    description = 'D of KDJ'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        close = Close_Daily()
        high = High_Daily()
        low = Low_Daily()
        _, D, _ = KDJ(close, high, low)
        return D.load(instrument_id, time_range)
