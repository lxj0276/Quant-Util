from feature.base import PersistentFeature
from feature.zoo.Close_Daily import Close_Daily
from feature.zoo.High_Daily import High_Daily
from feature.zoo.Low_Daily import Low_Daily

from .ADX import ADX


class ADX_Daily(PersistentFeature):
    description = '衡量市场趋势是否稳固，数值越大趋势越稳'
    formula = '(1）+DM=本日最高-前日最高 & -DM=前日最低-本日最低；比较+DM和-DM，较小的置为0 （2）真实波幅TR 以下三项取绝对值最大者：当日最高-当日最低；当日最高-前日收盘；当日最低-前日收盘 （3）方向线DI 将±DM和TR做N（N=12）日平均，得到±DM12和TR12，±DI=（±DM12/TR12)*100 （4）动向平均数ADX DX=±DI之差/±DI之和 * 100 ADX是DX的移动平均'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        close = Close_Daily()
        high = High_Daily()
        low = Low_Daily()
        adx = ADX(close, high, low)
        return adx.load(instrument_id, time_range)
