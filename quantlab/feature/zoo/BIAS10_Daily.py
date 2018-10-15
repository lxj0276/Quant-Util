from quantlab.feature import *
from quantlab.feature.ops import Div, Sub


class BIAS10_Daily(PersistentFeature):

    description = '均线衍生指标，BIAS有回归0的趋势'
    formula = '(Close-MA10)/MA10'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        return Div(Sub(Close_Daily(), MA10_Daily()), MA10_Daily()).load(instrument_id, time_range)
