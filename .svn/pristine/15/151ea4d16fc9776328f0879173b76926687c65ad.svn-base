from quantlab.feature import *
from .PSY import PSY


class PSY_Daily(PersistentFeature):

    description = '多空指标，psy小于20为空头市场，大于80为多头市场'
    formula = 'PSY=N日内上涨天数/N*100, N=12'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        close = Close_Daily()
        psy = PSY(close, 12)
        return psy.load(instrument_id, time_range)
