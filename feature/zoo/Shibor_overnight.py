from feature.base import InstrumentIDUnRelated, PersistentFeature

from feature.error import OriginalFeatureError


class Shibor_overnight(InstrumentIDUnRelated, PersistentFeature):
    description = '上海银行间同业拆放利率（隔夜）'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')
