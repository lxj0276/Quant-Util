from feature.base import PersistentFeature
from feature.zoo.Close_Daily import Close_Daily

from .CMO import CMO


class CMO5(PersistentFeature):
    description = 'CMO指标是寻找极度超买和极度超卖的条件'
    formula = 'CMO = （Su - Sd) × 100 / (Su + Sd) 其中：Su是今日收盘价与昨日收盘价（上涨日）差值加总。若当日下跌，则增加值为0；Sd是今日收盘价与做日收盘价（下跌日）差值的绝对值加总。若当日上涨，则增加值为0；'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        close = Close_Daily()
        return CMO(close, 5).load(instrument_id, time_range)
