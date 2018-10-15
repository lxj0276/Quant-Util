from quantlab.feature import *
from .Aroon import Aroon


class AroonDown_Daily(PersistentFeature):

    description = '阿隆up和down应结合使用，若两者平行则市场维持原趋势，两者交叉则趋势反转'
    formula = 'AroonDown = window中最高价前天数/总天数*100'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        price = Low_Daily()
        aroondown = Aroon(price, down=True, window=25)
        return aroondown.load(instrument_id, time_range)
