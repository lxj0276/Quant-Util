# -*- coding: utf-8 -*-
from quantlab.feature import PersistentFeature, NonPersistentFeature
from quantlab.feature.error import OriginalFeatureError

class Net_margin(PersistentFeature):
    description = '扣除非经常损益后的净利润率'
    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
