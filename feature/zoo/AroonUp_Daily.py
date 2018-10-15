from feature.base import PersistentFeature
from feature.zoo.High_Daily import High_Daily

from .Aroon import Aroon


class AroonUp_Daily(PersistentFeature):
    description = '阿隆up和down应结合使用，若两者平行则市场维持原趋势，两者交叉则趋势反转'
    formula = 'AroonUp = window中最低价前天数/总天数*100'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        price = High_Daily()
        aroonup = Aroon(price, down=False, window=25)
        return aroonup.load(instrument_id, time_range)
