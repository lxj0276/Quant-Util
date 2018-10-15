from feature.base import PersistentFeature
from feature.zoo.ChangeRate_Daily import ChangeRate_Daily

from .CVAR import CVAR


class CVAR_normal_Daily(PersistentFeature):
    description = '表示极端情况下亏损情况，通常情况下是负值，越小风险越大'
    formula = 'CVAR 计算前window天（包括今天）收益率的均值和方差,并认为收益率分布符合正态分布，在负无穷到mu-2sigma范围内,对收益率按正态分布积分。'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        return CVAR(ChangeRate_Daily()).load(instrument_id, time_range)
