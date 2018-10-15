# -*- coding: utf-8 -*-
from quantlab.feature import PersistentFeature, NonPersistentFeature
from quantlab.feature.error import OriginalFeatureError

class Final_balance_of_cash_and_cash_equivalents(PersistentFeature):
    description = '期末现金及现金等价物余额'
    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
