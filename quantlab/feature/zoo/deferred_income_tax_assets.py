﻿# -*- coding: utf-8 -*-
from quantlab.feature import PersistentFeature, NonPersistentFeature
from quantlab.feature.error import OriginalFeatureError

class Deferred_income_tax_assets(PersistentFeature):
    description = '递延所得税资产'
    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
