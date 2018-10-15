from quantlab.feature import *
from quantlab.feature.ops import *


class MACD_Daily(PersistentFeature):

    description = 'MACD由负转正，是买的信号。MACD由正转负，是卖的信号'
    formula = 'MACD=2*(DIFF-DEA)'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        return Sub(DIFF_Daily(), DEA_Daily()).load(instrument_id, time_range)*2
