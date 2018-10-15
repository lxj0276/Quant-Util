from quantlab.feature import *
from .BOLL import BOLL


class BOLLUp_Daily(PersistentFeature):

    description = '均线衍生指标，股价倾向于在上下布林线之间'
    formula = 'MA20+2*Std20'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        close = Close_Daily()
        bollup = BOLL(close, down=False)
        return bollup.load(instrument_id, time_range)
