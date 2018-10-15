import requests
import pandas as pd
from tqdm import tqdm

class juchao_api:
    balance_sheet_url = 'http://webapi.cninfo.com.cn/api/stock/p_stock2300'
    profit_sheet_url='http://webapi.cninfo.com.cn/api/stock/p_stock2301'
    cashflow_sheet_url='http://webapi.cninfo.com.cn/api/stock/p_stock2302'
    financial_indicator_url='http://webapi.cninfo.com.cn/api/stock/p_stock2303'

    client_id = '825012849ef5409ca966fff5e2540dc2'
    client_secret = '2353fd9fb5414740bb4bcc71bbdafb41'

    token_url = 'http://webapi.cninfo.com.cn/api-cloud-platform/oauth2/token'
    def __init__(self):
        self.token=self.get_token()

    def get_token(self):
        post_data = {'client_id': self.client_id, 'client_secret': self.client_secret,
                     'grant_type': 'client_credentials'}
        headers={"Host":"webapi.cninfo.com.cn",
                 "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                 "Origin":"http://webapi.cninfo.com.cn"}
        response = requests.post(self.token_url,headers=headers, data=post_data)
        if response.status_code != 200:
            raise ValueError("get token error ")
        return response.json()['access_token']

    def get_sheet(self,stockIds,sheet_url):
        scode_lists = [','.join(stockIds[i * 50:(i + 1) * 50]) for i in range(len(stockIds) // 50+1)]

        dfs = []
        for scode in tqdm(scode_lists):
            param = {'scode': scode, "access_token": self.token}
            data = requests.get(sheet_url, params=param)
            df = pd.DataFrame(data.json()["records"])
            dfs.append(df)
        df = pd.concat(dfs, axis=0)

        df.insert(0, 'date', df['DECLAREDATE'].map(lambda x: x.replace('-', '')).astype(int))
        df.insert(1, 'instrument_id', df['SECCODE'].map(
            lambda x: "CN_STK_{}{}".format('SH', x) if x[0] == "6" else"CN_STK_{}{}".format('SZ', x)))
        df.insert(2, 'financial_period', df['ENDDATE'].map(lambda x: int(x[:4]) * 10 + int(x[5:7]) / 3).astype(int))
        return df

    def get_sheet_without_DECLAREDATE(self,stockIds,sheet_url):
        scode_lists = [','.join(stockIds[i * 50:(i + 1) * 50]) for i in range(len(stockIds) // 50+1)]

        dfs = []
        for scode in tqdm(scode_lists):
            param = {'scode': scode, "access_token": self.token}
            data = requests.get(sheet_url, params=param)
            df = pd.DataFrame(data.json()["records"])
            dfs.append(df)
        df = pd.concat(dfs, axis=0)

        # df.insert(0, 'date', df['DECLAREDATE'].map(lambda x: x.replace('-', '')).astype(int))
        df.insert(0, 'instrument_id', df['SECCODE'].map(
            lambda x: "CN_STK_{}{}".format('SH', x) if x[0] == "6" else"CN_STK_{}{}".format('SZ', x)))
        df.insert(1, 'financial_period', df['ENDDATE'].map(lambda x: int(x[:4]) * 10 + int(x[5:7]) / 3).astype(int))
        return df


if __name__=="__main__":
    from feature import *
    from mongoapi.utils import df_to_mongo
    from mongoapi.config import FUNDAMENTAL_DB,PROFIT_SHEET,BALANCE_SHEET,CASHFLOW_SHEET,FINANCIAL_INDICATOR_SHEET
    stockIds=list(map(lambda x:x[-6:],list_instrument_ids(instrument_type='STK')))
    s=juchao_api()


    from mongoapi.env import BALANCE_SHEET_COLLECTION
    records=BALANCE_SHEET_COLLECTION.find()
    df1=list(records)
    df1=pd.DataFrame(df1)
    df1=df1[['instrument_id','date','financial_period']]
    df = s.get_sheet_without_DECLAREDATE(stockIds, s.financial_indicator_url)
    df2=df.merge(df1,on=['instrument_id','financial_period'],how='inner')
    df2['date']=df2['date'].astype(int)
    df_to_mongo(df2, FUNDAMENTAL_DB, FINANCIAL_INDICATOR_SHEET, indexes=[[('date', 1), ('instrument_id', 1)], 'financial_period'],if_exists='ignore')

    df=s.get_sheet(stockIds,s.cashflow_sheet_url)
    df_to_mongo(df,FUNDAMENTAL_DB,CASHFLOW_SHEET,indexes=[[('date',1),('instrument_id',1)],'financial_period'])

    df=s.get_sheet(stockIds,s.profit_sheet_url)
    df_to_mongo(df,FUNDAMENTAL_DB,PROFIT_SHEET,indexes=[[('date',1),('instrument_id',1)],'financial_period'])

    df=s.get_sheet(stockIds,s.balance_sheet_url)
    df_to_mongo(df,FUNDAMENTAL_DB,BALANCE_SHEET,indexes=[[('date',1),('instrument_id',1)],'financial_period'])

    df=s.get_sheet(stockIds[:2], s.balance_sheet_url)
    df.to_csv('/data/test.csv',encoding='gbk')
