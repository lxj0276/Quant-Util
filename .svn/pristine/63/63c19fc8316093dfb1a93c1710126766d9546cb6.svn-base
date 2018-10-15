from feature.base import PersistentFeature
from feature.ops import *
from feature.zoo.Close_Daily import Close_Daily


class EMA60_Daily(PersistentFeature):
    description = '60-day Exponentially-weighted moving average of daily close price feature'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        return EMA(Close_Daily(), 60).load(instrument_id, time_range)
