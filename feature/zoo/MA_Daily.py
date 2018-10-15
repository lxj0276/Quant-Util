from feature.base import PersistentFeature
from feature.ops import *
from feature.zoo.Close_Daily import Close_Daily


class MA_Daily(PersistentFeature):
    description = 'N-day moving average of daily close price feature'

    granularity = 'day'

    def __init__(self, window):
        self.window = window

    def _create_feature(self, instrument_id, time_range):
        return MA_skipna(Close_Daily(), self.window).load(instrument_id, time_range)
