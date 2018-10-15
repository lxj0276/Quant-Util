# -*- coding: utf-8 -*-
from quantlab.feature import PersistentFeature, NonPersistentFeature
from quantlab.feature.error import OriginalFeatureError

class Neu_RE_P(PersistentFeature):
    description = 'RE_P＝剔除非经常损益后的净利润/市值'
    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
