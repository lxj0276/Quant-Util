# -*- coding: utf-8 -*-
from quantlab.feature import PersistentFeature, NonPersistentFeature
from quantlab.feature.error import OriginalFeatureError

class Administration_expense_cost(PersistentFeature):
    description = '管理费用'
    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
