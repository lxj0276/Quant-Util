from feature.base import PersistentFeature
from feature.zoo.Close_Daily import Close_Daily
from feature.zoo.High_Daily import High_Daily
from feature.zoo.Low_Daily import Low_Daily
from feature.zoo.Money_Daily import Money_Daily

from .MFI import MFI


class MFI_Daily(PersistentFeature):
    description = 'MFI 表征资金流向，向上突破20表示资金转热，可以买入。向下突破80表示资金转冷，应当卖出'
    formula = 'TP=mean(high+low+close), PositiveMoneyFlow is the sum(Money) in 14days when TP is greater than last day. The same NegativeMoneyFlow. MFR=PMF/NMF, MFI=100-100/(1+MFR)'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        close = Close_Daily()
        high = High_Daily()
        low = Low_Daily()
        money = Money_Daily()
        mfi = MFI(close, high, low, money, window=14)
        return mfi.load(instrument_id, time_range)
