# -*- coding: utf-8 -*-
from quantlab.feature import PersistentFeature, NonPersistentFeature, InstrumentIDUnRelated
from quantlab.feature.error import OriginalFeatureError

class Shibor_1month(InstrumentIDUnRelated, PersistentFeature):
    description = '上海银行间同业拆放利率（1个月）'
    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')