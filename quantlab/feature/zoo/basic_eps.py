﻿# -*- coding: utf-8 -*-
from quantlab.feature import PersistentFeature, NonPersistentFeature
from quantlab.feature.error import OriginalFeatureError

class Basic_eps(PersistentFeature):
    description = '（一）基本每股收益'
    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
