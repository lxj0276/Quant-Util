from feature.base import PersistentFeature

from feature.error import *


class G_NeToperateCashFlow(PersistentFeature):
    description = '经营活动现金流净值增长率'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
