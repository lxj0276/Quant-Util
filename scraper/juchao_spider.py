import requests
import pandas as pd
from zipfile import ZipFile
from io import BytesIO
from scraper.proxy_generator import proxy_generator
from requests.exceptions import ProxyError
from requests.exceptions import ConnectTimeout,ReadTimeout
from retry import retry



class juchao_spider:
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
        "Host": "www.cninfo.com.cn"}
    request_url='http://www.cninfo.com.cn/cninfo-new/data/download'
    def __init__(self):
        self.proxy_generator=proxy_generator()
        self.proxy_ip=[]
    def get_proxy(self):
        if len(self.proxy_ip)>0:
            return self.proxy_ip.pop()
        else:
            self.proxy_ip=self.proxy_generator.generate()
        return self.proxy_ip.pop()

    @classmethod
    def post_data(cls,code,type,minYear,maxYear):
        market='sh' if code[0]=="6" else 'sz'
        post_data = {"market": market,
                     "type": type,
                     "code": code,
                     "orgid": 'gs'+market+code,
                     "minYear": minYear,
                     "maxYear": maxYear}
        return post_data

    @retry(exceptions=(ProxyError,ConnectTimeout,ReadTimeout),tries=10)
    def get_records(self,code,type,minYear,maxYear,use_proxy=False):
        post_data=self.post_data(code,type,minYear,maxYear)
        if use_proxy:
            proxy_ip=self.get_proxy()
            proxy={'http': 'http://'+proxy_ip}
            response = requests.post(self.request_url, headers=self.header, data=post_data,proxies = proxy,timeout=10)
        else: response = requests.post(self.request_url, headers=self.header, data=post_data)
        zip_file = ZipFile(BytesIO(response.content))
        tables=zip_file.namelist()
        df = pd.concat(map(lambda x:pd.read_csv(BytesIO(zip_file.read(x)),dtype={'机构ID':str}, encoding='gbk'),tables))
        df['机构ID']=df['机构ID'].str.replace('\t','')
        df=df.rename(columns={'机构ID':'instrument_id','公告日期':'reportDate',"截止日期":'financialPeriod'})
        df['financialPeriod']=df['financialPeriod'].map(lambda x:int(x[:4])*10+int(x[5:7])//3 ).astype(int)
        return df



