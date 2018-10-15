from feature.base import PersistentFeature
from feature.ops import *
from feature.zoo.Close_Min import Close_Min
from feature.zoo.Recovery_Factor import Recovery_Factor


class Close_Min_Hfq(PersistentFeature):
    description = 'minute close price feature,后复权'

    granularity = 'minute'

    def _create_feature(self, instrument_id, time_range):
        recovery_factor = Recovery_Factor()
        clo_min = Close_Min()
        return Mul_MD(clo_min, recovery_factor).load(instrument_id, time_range)
