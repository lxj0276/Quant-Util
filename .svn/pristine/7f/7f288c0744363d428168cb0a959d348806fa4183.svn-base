from quantlab.feature import *
from .EMV import EMV

class EMV_Daily(PersistentFeature):

    description = '表现主力资金控盘程度，应与其MA共同使用'
    formula = 'PR=(最高价+最低价)/2-(前日最高价+前日最低价)/2 PV=Money /（最高价-最低价）EMV=PR/PV'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        high = High_Daily()
        low = Low_Daily()
        money = Money_Daily()
        emv = EMV(high, low, money, 14)
        return emv.load(instrument_id, time_range)
