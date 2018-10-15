# -*- coding: utf-8 -*-
from quantlab.feature import PersistentFeature, NonPersistentFeature
from quantlab.feature.error import OriginalFeatureError

class Total_profit(PersistentFeature):
    description = '四、利润总额'
    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
