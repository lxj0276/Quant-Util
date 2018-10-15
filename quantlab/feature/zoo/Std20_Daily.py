from quantlab.feature import *
from quantlab.feature.ops import *


class Std20_Daily(PersistentFeature):

    description = '20 day close price standard deviation'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        return Vola(Close_Daily(), 20).load(instrument_id, time_range)
