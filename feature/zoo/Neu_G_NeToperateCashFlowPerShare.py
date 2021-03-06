from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Neu_G_NeToperateCashFlowPerShare(PersistentFeature):
    description = '每股经营活动净现金流增长率'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
