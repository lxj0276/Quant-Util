import os
from collections import OrderedDict

import pandas as pd
from engine.cons import *
from engine.utils import get_calendar
from feature.time import TimeRange
from mongoapi.get_data import get_day_trade_data
from redis_cache.rediscache import cache_it_pickle


class pricing_data_loader:
    def __init__(self, load_path=PRICING_DATA_PATH):
        self.load_path = load_path

    def load_data(self, instruments, feature, start_time, end_time):
        pass

    #
    # @cache_it_pickle()
    # def load_single_data(self, instrument, start_time, end_time, feature='close'):
    #     df = pd.read_csv(os.path.join(self.load_path, instrument + '.csv'))[['date', feature, 'rate']]
    #     df = df.rename(columns={feature: PRICE})
    #     # df[PRICE]=df[PRICE]/df['rate']
    #     del df['rate']
    #     carlender = get_calendar()
    #
    #     df = df.set_index('date')
    #     df_full = df.reindex(carlender).fillna(method='ffill')
    #
    #     pricing_data = df_full[(df_full.index >= start_time) & (df_full.index <= end_time)].to_dict()[PRICE]
    #     df = df.reindex(df_full.index)
    #     on_trading = (~df[(df.index >= start_time) & (df.index <= end_time)].isnull()).astype(int).to_dict()[PRICE]
    #     return OrderedDict(pricing_data), OrderedDict(on_trading)
    @cache_it_pickle()
    def load_single_data(self, instrument, start_time, end_time, feature='close'):
        trade_calendar = get_calendar(start_time, end_time)
        data = get_day_trade_data([instrument],
                                  start_time,
                                  end_time,
                                  [feature],
                                  return_df=True)[['date',feature]].set_index('date')
        data=data.reindex(trade_calendar)
        pricing_data = data.fillna(method='ffill').to_dict()[feature]
        on_trading = (~data.isnull()).astype(int).to_dict()[feature]
        return OrderedDict(pricing_data), OrderedDict(on_trading)


