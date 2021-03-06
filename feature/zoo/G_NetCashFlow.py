from feature.base import PersistentFeature

from feature.error import *


class G_NetCashFlow(PersistentFeature):
    description = '净现金流增长率'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
