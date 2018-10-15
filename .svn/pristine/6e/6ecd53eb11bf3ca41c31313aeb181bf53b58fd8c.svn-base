from feature.base import PersistentFeature
from feature.zoo.ChangeRate_Daily import ChangeRate_Daily

from .Sharpe import Sharpe


class Sharpe40_Daily(PersistentFeature):
    description = 'sharpe表示收益的稳健程度，越大越好'
    formula = 'Sharpe = 收益率均值/方差'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        change = ChangeRate_Daily()
        sharpe = Sharpe(change, window=40)
        return sharpe.load(instrument_id, time_range)
