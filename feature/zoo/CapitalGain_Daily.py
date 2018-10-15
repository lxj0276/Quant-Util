from feature.base import PersistentFeature
from feature.ops import *
from feature.zoo.Close_Daily import Close_Daily
from feature.zoo.ReferencePrice_Daily import ReferencePrice_Daily


class CapitalGain_Daily(PersistentFeature):
    description = '（广发证券）在Grinblatt(2005)个股参考价格的基础上，与当日股价相比较得到了资本利得突出量'
    formula = 'Capital_Gain_Overhang = (Close_Daily-RP)/RP'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        price = Shift(Close_Daily(), 1)
        RP = ReferencePrice_Daily()
        CGO = Div(Sub(price, RP), RP)
        return CGO.load(instrument_id, time_range)
