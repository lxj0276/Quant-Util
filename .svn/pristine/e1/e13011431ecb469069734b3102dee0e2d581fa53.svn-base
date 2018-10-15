from feature.base import PersistentFeature
from feature.ops import *
from feature.zoo.Close_Daily import Close_Daily

class Return_Daily(PersistentFeature):
    description = 'Daily_return'

    granularity = 'day'
    def _create_feature(self, instrument_id, time_range):
        return Sub(Div(Shift(Close_Daily(),-1),Close_Daily()),1).load( instrument_id, time_range)

class Return_NDay(PersistentFeature):
    description = 'Daily_return'

    granularity = 'day'

    def __init__(self,lag_period):
        self.lag_period=lag_period

    def __str__(self):
        return "{}({})" .format(self.name,self.lag_period)

    def _create_feature(self, instrument_id, time_range):
        return Sub(Div(Shift(Close_Daily(),-self.lag_period),Close_Daily()),1).load( instrument_id, time_range)


class Return_NDay_Label(Return_NDay):
    description = 'Daily_return 二值化后'

    granularity = 'day'

    def __init__(self, lag_period):
        self.lag_period = lag_period

    def __str__(self):
        return "{}({})".format(self.name, self.lag_period)

    def _create_feature(self, instrument_id, time_range):
        data=super(Return_NDay_Label,self)._create_feature(instrument_id,time_range)
        data=data.applymap(lambda x:1 if x>=0 else 0)
        return data
