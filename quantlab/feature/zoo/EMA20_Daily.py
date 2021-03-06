from quantlab.feature import *
from quantlab.feature.ops import *


class EMA20_Daily(PersistentFeature):

    description = '20-day Exponentially-weighted moving average of daily close price feature'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        return EMA(Close_Daily(), 20).load(instrument_id, time_range)
