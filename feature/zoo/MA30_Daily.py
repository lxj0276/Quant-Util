from feature.base import PersistentFeature
from feature.ops import *
from feature.zoo.Close_Daily import Close_Daily


class MA30_Daily(PersistentFeature):
    description = '30-day moving average of daily close price feature'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        return MA_skipna(Close_Daily(), 30).load(instrument_id, time_range)
