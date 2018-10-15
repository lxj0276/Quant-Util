from quantlab.feature import *
from .ROC import ROC


class ROC_Daily(PersistentFeature):

    description = '动量指标，无量纲，与其MA配合使用。'
    formula = 'ROC=(close/close_12d_before - 1)*100'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        close = Close_Daily()
        return ROC(close, 12).load(instrument_id, time_range)
