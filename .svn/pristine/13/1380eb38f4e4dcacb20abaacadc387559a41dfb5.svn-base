from feature.base import PersistentFeature
from feature.ops import *
from feature.zoo.Close_Daily import Close_Daily


class DIFF_Daily(PersistentFeature):
    description = 'DIFF=EMA12-EMA26'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        return Sub(EMA(Close_Daily(), 12), EMA(Close_Daily(), 26)).load(instrument_id, time_range)
