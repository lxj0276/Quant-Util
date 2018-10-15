# -*- coding: utf-8 -*-
from quantlab.feature import PersistentFeature, NonPersistentFeature
from quantlab.feature.error import OriginalFeatureError

class Net_cash_flow_for_operating_activities(PersistentFeature):
    description = '经营活动产生的现金流量净额'
    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
