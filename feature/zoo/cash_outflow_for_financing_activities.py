from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Cash_outflow_for_financing_activities(PersistentFeature):
    description = '筹资活动现金流出小计'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
