from quantlab.feature import *
from quantlab.feature.ops import *


class MA10_Daily(PersistentFeature):

    description = '10-day moving average of daily close price feature'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        return MA(Close_Daily(), 10).load(instrument_id, time_range)
