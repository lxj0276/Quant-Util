# -*- coding: utf-8 -*-
from quantlab.feature import PersistentFeature, NonPersistentFeature
from quantlab.feature.error import OriginalFeatureError

class Subsidize_revenue(PersistentFeature):
    description = '加：补贴收入'
    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
