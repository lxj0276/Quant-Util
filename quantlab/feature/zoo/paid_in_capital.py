﻿# -*- coding: utf-8 -*-
from quantlab.feature import PersistentFeature, NonPersistentFeature
from quantlab.feature.error import OriginalFeatureError

class Paid_in_capital(PersistentFeature):
    description = '实收资本（或股本）'
    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
