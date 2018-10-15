from engine.utils import get_calendar

class industry:
    stock_industry_dict=dict()
    industry_stock_dict=dict()
    __loaded=None

    @classmethod
    def get_industry(cls,stockId):
        if not cls.__loaded:
            cls._load()
        return cls.stock_industry_dict[stockId]
    @classmethod
    def get_stocks(cls,industry):
        if not cls.__loaded:
            cls._load()
        return cls.industry_stock_dict[industry]

    @classmethod
    def _load(cls):
        import tushare as ts
        df=ts.get_stock_basics()['industry'].reset_index().rename(columns={'code':'stockId'})
        df['stockId']=df['stockId'].map(lambda x:'CN_STK_SH'+x if x[0]=='6' else 'CN_STK_SZ'+x)
        cls.stock_industry_dict=df.set_index('stockId')['industry'].to_dict()
        for k,v in cls.stock_industry_dict.items():
            if v not in cls.industry_stock_dict.keys():
                cls.industry_stock_dict[v]=[k]
            else:
                cls.industry_stock_dict[v].append(k)
        cls.__loaded=True

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

def get_industry_return(industryID, start_time,end_time):
    from mongoapi.get_data import get_stock_return
    instrument_ids=industry.get_stocks(industryID)
    return get_stock_return(instrument_ids,start_time,end_time).mean(axis=1)


