from quantlab.feature import *
from quantlab.feature.error import *


class G_TotalAssets(PersistentFeature):
    description = '总资产增长率'
    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
