﻿from quantlab.feature import PersistentFeature
from quantlab.feature.error import OriginalFeatureError

class  Snowball_tweet(PersistentFeature):

    description = '某只股票的雪球累计讨论次数'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')