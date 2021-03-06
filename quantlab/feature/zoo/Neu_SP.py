# -*- coding: utf-8 -*-
from quantlab.feature import PersistentFeature, NonPersistentFeature
from quantlab.feature.error import OriginalFeatureError

class Neu_SP(PersistentFeature):
    description = 'SP＝营业收入/市值'
    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
