from feature.base import PersistentFeature
from feature.zoo.Close_Daily import Close_Daily
from feature.zoo.High_Daily import High_Daily
from feature.zoo.Low_Daily import Low_Daily

from .CCI import CCI


class CCI14_Daily(PersistentFeature):
    description = 'CCI指标针只对极端行情生效，适用于短线操作。当CCI越过±100时即极端行情，大于100做多，小于-100做空，回归±100区间时应平仓修整，等待下一次极端行情'
    formula = 'CCI=(TP-MA)/MD/0.015;TP=（最高价+最低价+收盘价）/3;MA=近N日移动平均;MD=近N日(MA-收盘价)移动平均'
    granularity = 'day'

    '''

    '''

    def _create_feature(self, instrument_id, time_range):
        close = Close_Daily()
        high = High_Daily()
        low = Low_Daily()
        cci = CCI(close, high, low, 14)
        return cci.load(instrument_id, time_range)
