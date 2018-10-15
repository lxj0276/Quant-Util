from feature.base import PersistentFeature
from feature.zoo.Close_Daily import Close_Daily

from .BOLL import BOLL


class BOLLDown_Daily(PersistentFeature):
    description = '均线衍生指标，股价倾向于在上下布林线之间'
    formular = 'MA20-2*Std20'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        close = Close_Daily()
        bolldown = BOLL(close, down=True)
        return bolldown.load(instrument_id, time_range)
