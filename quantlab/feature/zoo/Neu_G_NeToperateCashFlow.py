# -*- coding: utf-8 -*-
from quantlab.feature import PersistentFeature, NonPersistentFeature
from quantlab.feature.error import OriginalFeatureError

class Neu_G_NeToperateCashFlow(PersistentFeature):
    description = '经营活动现金流净值增长率'
    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
