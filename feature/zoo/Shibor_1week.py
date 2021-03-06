from feature.base import InstrumentIDUnRelated, PersistentFeature

from feature.error import OriginalFeatureError


class Shibor_1week(InstrumentIDUnRelated, PersistentFeature):
    description = '上海银行间同业拆放利率（1周）'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
