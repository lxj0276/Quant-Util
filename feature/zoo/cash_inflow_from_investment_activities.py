from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Cash_inflow_from_investment_activities(PersistentFeature):
    description = '投资活动现金流入小计'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
