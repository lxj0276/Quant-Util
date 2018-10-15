from feature.base import PersistentFeature
from feature.ops import *
from feature.error import OriginalFeatureError
from feature.zoo.revenue import Revenue
from feature.zoo.operating_expenses import Operating_expenses


class Gross_margin(PersistentFeature):
    description = '毛利润'

    def _create_feature(self, instrument_id, time_range):
        gm = Sub(Revenue(), Operating_expenses())
        return gm.load(instrument_id, time_range)
