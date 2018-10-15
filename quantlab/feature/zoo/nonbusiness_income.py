# -*- coding: utf-8 -*-
from quantlab.feature import PersistentFeature, NonPersistentFeature
from quantlab.feature.error import OriginalFeatureError

class Nonbusiness_income(PersistentFeature):
    description = '营业外收入'
    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
