from quantlab.feature import *
from quantlab.feature.ops import *


class DIFF_Daily(PersistentFeature):

    description = 'DIFF=EMA12-EMA26'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        return Sub(EMA(Close_Daily(), 12), EMA(Close_Daily(), 26)).load(instrument_id, time_range)
