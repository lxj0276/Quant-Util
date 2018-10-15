from quantlab.feature import *
from quantlab.feature.ops import *


class ChangeRate_Daily(NonPersistentFeature):

    description = '(close-close_1day_before)/close_1day_before// 0.01 means change 1%'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        close = Close_Daily()
        change_rate = Sub(Div(close, Shift(close, 1)), 1)
        return change_rate.load(instrument_id, time_range)
