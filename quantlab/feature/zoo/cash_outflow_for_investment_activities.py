# -*- coding: utf-8 -*-
from quantlab.feature import PersistentFeature, NonPersistentFeature
from quantlab.feature.error import OriginalFeatureError

class Cash_outflow_for_investment_activities(PersistentFeature):
    description = '投资活动现金流出小计'
    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
