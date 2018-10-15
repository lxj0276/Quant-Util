from datetime import datetime, timedelta
from engine.utils import get_calendar
import numpy as np
import pandas as pd

FREQUANCE_DAY='day'
FREQUANCE_MINUTE='minute'
FREQUANCE_TICK='tick'

def time_frequance(thetime):
    return FREQUANCE_TICK if thetime>10000101093003 else( FREQUANCE_DAY if thetime < 30000000 else FREQUANCE_MINUTE )# 判断并生成feature的频率



def time_shift_normal(thetime, shift_num):
    thetime = datetime.strptime(str(thetime), '%Y%m%d')
    thetime -= timedelta(days=shift_num)
    return int(thetime.strftime('%Y%m%d'))


def time_shift(thetime, shift_num):
    if time_frequance(thetime)==FREQUANCE_TICK:
        return thetime
    calendar = get_calendar()
    success, value = calendar.most_recent_up(thetime)
    if not success:
        print('warning: time_shift exceed')
    thetime_index = calendar.index(value)
    return calendar[min(max(0, thetime_index - shift_num), len(calendar) - 1)]

def time_calendar_reduce(left_time,right_time):
    calendar = get_calendar()
    success,left_time_c=calendar.most_recent_up(left_time)
    left_time_idx=calendar.index(left_time_c)
    success,right_time_c=calendar.most_recent_up(right_time)
    right_time_idx=calendar.index(right_time_c)
    return left_time_idx-right_time_idx

def time_reuce(left_time,right_time):
    left_time = datetime.strptime(str(left_time), '%Y%m%d')
    right_time = datetime.strptime(str(right_time), '%Y%m%d')
    return (left_time-right_time).days

class industry:
    stock_industry_dict = dict()
    industry_stock_dict = dict()
    __loaded = None

    @classmethod
    def get_industry(cls, stockId):
        if not cls.__loaded:
            cls._load()
        return cls.stock_industry_dict[stockId]

    @classmethod
    def get_stocks(cls, industry):
        if not cls.__loaded:
            cls._load()
        return cls.industry_stock_dict[industry]

    @classmethod
    def _load(cls):
        import tushare as ts
        df = ts.get_stock_basics()['industry'].reset_index().rename(columns={'code': 'stockId'})
        df['stockId'] = df['stockId'].map(lambda x: 'CN_STK_SH' + x if x[0] == '6' else 'CN_STK_SZ' + x)
        cls.stock_industry_dict = df.set_index('stockId')['industry'].to_dict()
        for k, v in cls.stock_industry_dict.items():
            if v not in cls.industry_stock_dict.keys():
                cls.industry_stock_dict[v] = [k]
            else:
                cls.industry_stock_dict[v].append(k)
        cls.__loaded = True

    @classmethod
    def get_all_industry(cls):
        if not cls.__loaded:
            cls._load()
        return list(cls.industry_stock_dict.keys())

    @classmethod
    def get_all_stocks(cls):
        if not cls.__loaded:
            cls._load()
        return list(cls.stock_industry_dict.keys())

    @classmethod
    def get_industry_daily_return(cls, industry, date):
        pass

    @classmethod
    def get_industry_range_return(cls, starttime, endtime):
        pass

def xarray_to_df(xar):
    shape=xar.shape
    dims=xar.dims
    instrument_ds=xar.instrument_id
    thedatetime=xar.datetime
    features=xar.feature

    instrument_ids_full=np.array(list(instrument_ds.values)*shape[0]).reshape((-1,1))
    thedatetime_full=np.dstack([thedatetime.values]*shape[1]).flatten().reshape((-1,1))


    data=xar.values.reshape((-1,shape[-1]))
    data_full=np.concatenate([instrument_ids_full,thedatetime_full,data],axis=1)
    df=pd.DataFrame(data_full,columns=['instrument_id','datetime']+list(features.values))
    df[list(features.values)]=df[list(features.values)].astype(float)
    return df

if __name__ == '__main__':
    industry.get_industry('CN_STK_SH600104')
