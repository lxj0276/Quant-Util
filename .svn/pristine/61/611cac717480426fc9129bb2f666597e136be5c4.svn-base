import pandas as pd
from engine.utils import get_calendar
from mongoapi.get_data import (get_minute_trade_data,
                               get_day_trade_data,
                               get_profit_sheet_data,
                               get_cashflow_sheet_data,
                               get_balance_sheet_data,
                               get_financial_indicator_sheet_data
                               )
from Jsmmap.jsmmap import get_tick_trade_data
from redis_cache.rediscache import cache_it_timeseries
NAME_MAP = {
    "Close_Tick" :"最新",
    "Tick_Absent":"tag",
    "Vol_Tick":"成交量",
    # Tick level1.5 vol
    "Ask_Vol_Tick1":"卖一量",
    "Ask_Vol_Tick2":"卖二量",
    "Ask_Vol_Tick3":"卖三量",
    "Ask_Vol_Tick4":"卖四量",
    "Ask_Vol_Tick5":"卖五量",
    "Bid_Vol_Tick1":"买一量",
    "Bid_Vol_Tick2":"买二量",
    "Bid_Vol_Tick3":"买三量",
    "Bid_Vol_Tick4":"买四量",
    "Bid_Vol_Tick5":"买五量",


    "Ask_Price_Tick1":"卖一价",
    "Ask_Price_Tick2":"卖二价",
    "Ask_Price_Tick3":"卖三价",
    "Ask_Price_Tick4":"卖四价",
    "Ask_Price_Tick5":"卖五价",
    "Bid_Price_Tick1": "买一价",
    "Bid_Price_Tick2": "买二价",
    "Bid_Price_Tick3": "买三价",
    "Bid_Price_Tick4": "买四价",
    "Bid_Price_Tick5": "买五价",

    'Close_Daily': 'close',
    'Open_Daily': 'open',
    'High_Daily':'high',
    'Low_Daily':'low',
    'Vol_Daily':'volume',
    'Recovery_Factor': 'rate',
    'TurnOver_Daily':'turnover',
    'TurnOver_Full_Daily':'turnover_full',
    'Close_Min': 'close',
    'Open_Min': 'open',
    'High_Min': 'high',
    'Low_Min': 'low',
    'Vol_Min': 'vol',
    'Money_Min': 'money',
    'Net_Profit':'F027N',
    'Financial_Period':'financial_period',
    'Total_assets':'F038N',
    'Total_Shares':'F062N',#后面的代码为巨潮代码
    'Inventory':'F015N',
    'Revenue':'F006N',
    'Operating_expenses':'F007N',
    'Total_current_assets':'F019N',
    'Net_cash_flow_for_operating_activities':'F015N',
    'Nonbusiness_income':'F020N',
    'Quick_ratio':'F043N',
    'Cash_ratio':'F044N',
    'Cost_of_sales':'F009N',
    'Nav':'F054N',
    'Inventory_turnover_ratio':'F023N',
    'Net_profit_growth_rate':'F053N',
    'Npr':'F017N',
    'Accounts_receivable':'F009N',
    'Accounts_payable':'F042N',
    'Bvps':'F008N',
    'Equity':'F070N',
    'Diluted_eps':'F005N',
    'Lev':'F041N',
    'Total_liabilities':'F061N'#总负债
}
ON_FEATURE_RESPONSE={
    "Close_Tick": get_tick_trade_data,
    "Tick_Absent": get_tick_trade_data,
    "Vol_Tick": get_tick_trade_data,
    # Tick level1.5 vol
    "Ask_Vol_Tick1": get_tick_trade_data,
    "Ask_Vol_Tick2": get_tick_trade_data,
    "Ask_Vol_Tick3": get_tick_trade_data,
    "Ask_Vol_Tick4": get_tick_trade_data,
    "Ask_Vol_Tick5": get_tick_trade_data,
    "Bid_Vol_Tick1": get_tick_trade_data,
    "Bid_Vol_Tick2": get_tick_trade_data,
    "Bid_Vol_Tick3": get_tick_trade_data,
    "Bid_Vol_Tick4": get_tick_trade_data,
    "Bid_Vol_Tick5": get_tick_trade_data,

    "Ask_Price_Tick1": get_tick_trade_data,
    "Ask_Price_Tick2": get_tick_trade_data,
    "Ask_Price_Tick3": get_tick_trade_data,
    "Ask_Price_Tick4": get_tick_trade_data,
    "Ask_Price_Tick5": get_tick_trade_data,
    "Bid_Price_Tick1": get_tick_trade_data,
    "Bid_Price_Tick2": get_tick_trade_data,
    "Bid_Price_Tick3": get_tick_trade_data,
    "Bid_Price_Tick4": get_tick_trade_data,
    "Bid_Price_Tick5": get_tick_trade_data,


    'Close_Daily':get_day_trade_data,
    'Open_Daily':get_day_trade_data,
    'High_Daily':get_day_trade_data,
    'Low_Daily':get_day_trade_data,
    'Vol_Daily':get_day_trade_data,
    'TurnOver_Daily':get_day_trade_data,
    'TurnOver_Full_Daily':get_day_trade_data,
    'Recovery_Factor': get_day_trade_data,#复权因子
    'Close_Min':get_minute_trade_data,
    'Open_Min':get_minute_trade_data,
    'High_Min':get_minute_trade_data,
    'Low_Min':get_minute_trade_data,
    'Vol_Min':get_minute_trade_data,
    'Money_Min':get_minute_trade_data,
    'Net_Profit':get_profit_sheet_data,#净利润
    'Total_assets':get_balance_sheet_data,#总资产
    'Total_Shares':get_balance_sheet_data,#总股本
    'Inventory':get_balance_sheet_data,#存货
    'Total_liabilities':get_balance_sheet_data,#总负债
    'Revenue':get_profit_sheet_data,#营业收入
    'Operating_expenses':get_profit_sheet_data,#营业支出
    'Total_current_assets':get_balance_sheet_data,#流动资产合计
    'Nonbusiness_income':get_profit_sheet_data,#营业外收入
    'Quick_ratio':get_financial_indicator_sheet_data,#速动比率
    'Cash_ratio':get_financial_indicator_sheet_data,#现金比率
    'Cost_of_sales':get_profit_sheet_data,#销售费用
    'Nav':get_financial_indicator_sheet_data,#净资产增长率
    'Npr':get_financial_indicator_sheet_data,#净利率
    'Accounts_payable':get_balance_sheet_data,#应付账款
    'Accounts_receivable':get_balance_sheet_data,#应收账款
    'Net_profit_growth_rate':get_financial_indicator_sheet_data,#净利润增长率
    'Inventory_turnover_ratio':get_financial_indicator_sheet_data,#存货周转率
    'Bvps':get_financial_indicator_sheet_data,#每股净资产
    'Equity':get_balance_sheet_data,#股东权益
    'Lev':get_financial_indicator_sheet_data,#资产负债率
    'Diluted_eps':get_financial_indicator_sheet_data,#稀释每股收益
    'Net_cash_flow_for_operating_activities':get_cashflow_sheet_data,#经营活动产生现金流量净额
    'Financial_Period':get_profit_sheet_data#注意，三个报表中都可以有Financial_Period
}

TICK_DATA=["Close_Tick",
           "Tick_Absent",
           "Vol_Tick",
           "Ask_Vol_Tick1",
           "Ask_Vol_Tick2",
           "Ask_Vol_Tick3",
           "Ask_Vol_Tick4",
           "Ask_Vol_Tick5",

           "Bid_Vol_Tick1",
           "Bid_Vol_Tick2",
           "Bid_Vol_Tick3",
           "Bid_Vol_Tick4",
           "Bid_Vol_Tick5",

           "Ask_Price_Tick1",
           "Ask_Price_Tick2",
           "Ask_Price_Tick3",
           "Ask_Price_Tick4",
           "Ask_Price_Tick5",

           "Bid_Price_Tick1",
           "Bid_Price_Tick2",
           "Bid_Price_Tick3",
           "Bid_Price_Tick4",
           "Bid_Price_Tick5",
           ]



def load_single_feature_from_mongo(instrument_idx,featurename,start_time,end_time):
    func=ON_FEATURE_RESPONSE[featurename]
    feature_db_name=NAME_MAP[featurename]
    if featurename in TICK_DATA:
        return func(instrument_idx,start_time,end_time,feature_db_name)
    else:
        return func(instrument_idx,start_time,end_time,[feature_db_name],return_df=False)[feature_db_name]


def load_is_original(feature_name):
    if feature_name in NAME_MAP.keys():
        return True
    return False

#@cache_it_timeseries(expire=60*60*2)
def load_single_feature_from_mongo_df(instrument_ids,featurename,start_time,end_time):
    import pandas as pd
    if not  featurename in TICK_DATA:
        df=pd.DataFrame(load_single_feature_from_mongo(instrument_ids,featurename,start_time,end_time))
        if ON_FEATURE_RESPONSE[featurename] in (get_profit_sheet_data,
                                                get_cashflow_sheet_data,
                                                get_balance_sheet_data,
                                                get_financial_indicator_sheet_data):
            df=df.fillna(method='ffill')
            df=df.reindex(get_calendar(start_time,end_time))
    else:
        df=load_single_feature_from_mongo(instrument_ids,featurename,start_time,end_time)
    return df
