# -*- coding: utf-8 -*-
from quantlab.feature import PersistentFeature, NonPersistentFeature
from quantlab.feature.error import OriginalFeatureError

class Neu_PE(PersistentFeature):
    description = 'PE＝市值/归属母公司股东净利润'
    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
