from quantlab.feature import *
from quantlab.feature.ops import *


class EMA5_Daily(PersistentFeature):

    description = '5-day Exponentially-weighted moving average of daily close price feature'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        return EMA(Close_Daily(), 5).load(instrument_id, time_range)
