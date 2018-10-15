from feature.base import PersistentFeature
from feature.ops import *
from feature.zoo.DIFF_Daily import DIFF_Daily


class DEA_Daily(PersistentFeature):
    description = 'DEA=EMA(DIFF)9'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        return EMA(DIFF_Daily(), 9).load(instrument_id, time_range)
