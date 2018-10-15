from quantlab.feature import *
from quantlab.feature.ops import *


class MA60_Daily(PersistentFeature):

    description = '60-day moving average of daily close price feature'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        return MA(Close_Daily(), 60).load(instrument_id, time_range)
