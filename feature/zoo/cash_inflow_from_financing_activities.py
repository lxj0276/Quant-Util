from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Cash_inflow_from_financing_activities(PersistentFeature):
    description = '筹资活动现金流入小计'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
