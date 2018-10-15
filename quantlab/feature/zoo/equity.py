# -*- coding: utf-8 -*-
from quantlab.feature import PersistentFeature, NonPersistentFeature
from quantlab.feature.error import OriginalFeatureError

class Equity(PersistentFeature):
    description = '股东权益'
    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
