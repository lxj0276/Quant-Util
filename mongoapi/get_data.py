import pandas as pd
import pymongo
from engine.utils import get_calendar
from mongoapi.config import (DB_INSTRUMENT_ID,
                             FEATURE_INSTRUMENT_ID,
                             DB_DATE,
                             DB_TIME,
                             DB_DATETIME,
                             DB_MINUTE,
                             FEATURE_DATETIME,
                             SHIFT_NUM,
                             DB_INSTRUMENT_ID_FUNDAMENTAL, )
from mongoapi.cxdict import dcxdict, mcxdict
from mongoapi.env import (MINUTE_COLLECTION,
                          DAY_COLLECTION,
                          INDEX_DAY_COLLECTION,
                          BALANCE_SHEET_COLLECTION,
                          CASHFLOW_SHEET_COLLECTION,
                          PROFIT_SHEET_COLLECTION,
                          FINANCIAL_INDICATOR_COLLECTION
                          )
from quantlab_utils.utils import time_shift


def get_record_code_time(stock_collection, StockCode, datetime):
    one = stock_collection.find_one({'code': str(StockCode), 'date': datetime})
    return one


def get_record_code_dayrange(stock_collection, StockCode, dayRange):
    '''
    :param StockCode: code for stock
    :param daterange: (start day, end day)
    :return: list of records
    '''
    start_day = dayRange[0]
    end_day = dayRange[1]
    records = stock_collection.find({'code': str(StockCode), 'date': {"$lte": end_day}, 'date': {"$gte": start_day}})
    return list(records)


def get_recordList_dayRange(stock_collection, StockCodeList, dayRange):
    pass


def getData2(stock_collection, StockCodeList, dayRange, fields):
    '''
    :param stock_collection:
    :param StockCodeList: list
    :param dayRange: list
    :param fileds: list
    :return: {filed:{stockid:{day:[]the fileds_list}}}
    '''
    StockCodeList = list(StockCodeList)
    dayRange = list(dayRange)
    fields = list(fields)
    true_fields = [1] * len(fields)
    projection_fields = dict(zip(fields, true_fields))
    projection_fields['code'] = 1
    projection_fields['date'] = 1
    projection_fields['_id'] = 0
    records = stock_collection.find({'code': {'$in': StockCodeList}, 'date': {'$in': dayRange}}, projection_fields)
    records = list(records)

    retdict = {}

    for field in fields:
        retdict[field] = {}
        for code in StockCodeList:
            retdict[field][code] = {}
            for day in dayRange:
                retdict[field][code][day] = None
    for record in records:
        tmp_code = record['code']
        tmp_date = record['date']
        for field_name in fields:
            field_val = record[field_name]
            retdict[field_name][tmp_code][tmp_date] = field_val

    return retdict


def getData(stock_collection, StockCodeList, dayRange, fields, ffill=True):
    '''
    :param stock_collection:
    :param StockCodeList: list
    :param dayRange: list
    :param fileds: list
    :return: {filed:{stockid:{day:[]the fileds_list}}}
    '''
    StockCodeList = list(StockCodeList)
    dayRange = list(dayRange)
    fields = list(fields)
    true_fields = [1] * len(fields)
    projection_fields = dict(zip(fields, true_fields))
    projection_fields['code'] = 1
    projection_fields['date'] = 1
    projection_fields['_id'] = 0
    records = stock_collection.find({'code': {'$in': StockCodeList}, 'date': {'$in': dayRange}}, projection_fields)
    records = list(records)

    retdict = {}

    for field in fields:
        retdict[field] = {}
        for code in StockCodeList:
            retdict[field][code] = {}
            for day in dayRange:
                retdict[field][code][day] = None

    for record in records:
        tmp_code = record['code']
        tmp_date = record['date']
        for field_name in fields:
            if field_name not in retdict:
                retdict[field_name] = {}
            field_val = record[field_name]
            if tmp_code not in retdict[field_name]:
                retdict[field_name][tmp_code] = {}
            retdict[field_name][tmp_code][tmp_date] = field_val

    return retdict


def getData_V2(stock_collection, StockCodeList, start_day, end_day, fields, ffill=True):
    '''
    :param stock_collection:
    :param StockCodeList: list
    :param dayRange: list
    :param fileds: list
    :return: {filed:{stockid:{day:[]the fileds_list}}}

    for date search, use $gt $lt instead of $in
    '''
    StockCodeList = list(StockCodeList)

    start_date = start_day - 1
    end_date = end_day
    fields = list(fields)
    true_fields = [1] * len(fields)
    projection_fields = dict(zip(fields, true_fields))
    projection_fields['code'] = 1
    projection_fields['date'] = 1
    projection_fields['_id'] = 0
    records = stock_collection.find({'code': {'$in': StockCodeList}, 'date': {'$gt': start_date, '$lt': end_date}},
                                    projection_fields)
    records = list(records)

    retdict = {}

    for field in fields:
        retdict[field] = {}
        for code in StockCodeList:
            retdict[field][code] = {}
            for day in dayRange:
                retdict[field][code][day] = None

    for record in records:
        tmp_code = record['code']
        tmp_date = record['date']
        for field_name in fields:
            if field_name not in retdict:
                retdict[field_name] = {}
            field_val = record[field_name]
            if tmp_code not in retdict[field_name]:
                retdict[field_name][tmp_code] = {}
            retdict[field_name][tmp_code][tmp_date] = field_val

    return retdict


def getDataForIndustry(stock_collection, StockCodeList, dayRange, fields):
    '''
    :param stock_collection:
    :param StockCodeList: list
    :param dayRange: list
    :param fileds: list
    :return: {filed:{stockid:{day:[]the fileds_list}}}
    '''
    StockCodeList = list(StockCodeList)
    dayRange = list(dayRange)
    fields = list(fields)
    true_fields = [1] * len(fields)
    projection_fields = dict(zip(fields, true_fields))
    projection_fields['code'] = 1
    projection_fields['date'] = 1
    projection_fields['_id'] = 0
    records = stock_collection.find({'code': {'$in': StockCodeList}, 'date': {'$in': dayRange}}, projection_fields)
    records = list(records)
    return records


def getDataFromDayDB(StockCodeList, dayRange, fields):
    conn = pymongo.MongoClient('localhost', MONGODB_PORT)
    db = conn[MONGODB_DB]
    col = db[MONGODB_COLLECTION_DAY]
    return getData(col, StockCodeList, dayRange, fields)


def getDataFromMinuteDB(StockCodeList, dayRange, fields):
    conn = pymongo.MongoClient('localhost', MONGODB_PORT)
    db = conn[MONGODB_DB]
    col = db[MONGODB_COLLECTION_MINUTE]
    return getData(col, StockCodeList, dayRange, fields)


def get_daily_proposal_value(daily_proposal, date):
    stockID_list = list(daily_proposal.keys())
    fields = ['close']
    dayRange = [date]
    close_data = getData(DAY_COLLECTION, stockID_list, dayRange, fields)
    # data  { filed: {stockid: {day: []the fileds_list}}}
    # return close_data
    default_close = 0
    return sum([(close_data['close'][stockID][date] if close_data['close'][stockID][
                                                           date] is not None else default_close) * daily_proposal[
                    stockID] for stockID in stockID_list])


def get_daily_index_value(indexID, date):
    instrument_ids = [indexID]
    dayRange = [date]
    fields = ['close']
    # {filed:{stockid:{day:[]the fileds_list}}}
    data = getData(INDEX_DAY_COLLECTION, instrument_ids, dayRange, fields)
    return data['close'][indexID][date]


def get_index_return(instrument_ids, start_time, end_time):
    """
    get the return data for stocks in timerange
    :param instrument_ids:
    :param start_time:
    :param end_time:
    :return:
    """
    data = getData(INDEX_DAY_COLLECTION, instrument_ids, get_calendar(start_time, end_time), ['close'])
    df = pd.DataFrame(data['close'])
    df = (df / df.shift(1)).iloc[1:] - 1
    df = df.reindex(get_calendar(start_time, end_time))
    return df.fillna(0)


# ---------------------------------------below was written by liulongxiao--------------------------
def get_day_trade_data(instrument_ids, start_time, end_time, fields, return_df=True):
    """

    :param instrument_ids:
    :param time_range:
    :param fields:
    :return:
    """
    # TODO:check global conn valid

    StockCodeList = list(instrument_ids)
    dayRange = get_calendar(start_time, end_time)
    fields = list(fields)
    true_fields = [1] * len(fields)
    projection_fields = dict(zip(fields, true_fields))
    projection_fields[DB_INSTRUMENT_ID] = 1
    projection_fields[DB_DATE] = 1
    projection_fields['_id'] = 0
    records = DAY_COLLECTION.find({DB_INSTRUMENT_ID: {'$in': StockCodeList}, DB_DATE: {'$in': dayRange}},
                                  projection_fields)
    records = list(records)
    #############make shape all the same
    if not return_df:
        retdict = dcxdict()
        for field in fields:
            retdict[field] = {}
            for code in StockCodeList:
                retdict[field][code] = {}
                for day in dayRange:
                    retdict[field][code][day] = None

        for record in records:
            tmp_code = record[DB_INSTRUMENT_ID]
            tmp_date = record[DB_DATE]
            for field_name in fields:
                if field_name not in retdict:
                    retdict[field_name] = {}
                field_val = record[field_name]
                if tmp_code not in retdict[field_name]:
                    retdict[field_name][tmp_code] = {}
                retdict[field_name][tmp_code][tmp_date] = field_val
        return retdict
    else:
        df = pd.DataFrame(records)
        df = df.rename(columns={DB_INSTRUMENT_ID: FEATURE_INSTRUMENT_ID})
        return df


def get_minute_trade_data(instrument_ids, start_time, end_time, fields, return_df=True):
    """

    :param instrument_ids:
    :param time_range:
    :param fields:
    :return:
    """
    # TODO:check global conn valid

    StockCodeList = list(instrument_ids)
    dayRange = get_calendar(start_time, end_time)
    fields = list(fields)
    true_fields = [1] * len(fields)
    projection_fields = dict(zip(fields, true_fields))
    projection_fields[DB_INSTRUMENT_ID] = 1
    projection_fields[DB_DATE] = 1
    # projection_fields[DB_TIME] = 1
    projection_fields[DB_MINUTE] = 1
    projection_fields['_id'] = 0
    records = MINUTE_COLLECTION.find({DB_INSTRUMENT_ID: {'$in': StockCodeList}, DB_DATE: {'$in': dayRange}},
                                     projection_fields)
    records = list(records)
    if not return_df:
        retdict = mcxdict()

        for record in records:
            tmp_code = record[DB_INSTRUMENT_ID]
            tmp_date = record[DB_DATE]
            tmp_minute = record[DB_MINUTE]
            # tmp_minute = int(record[DB_TIME].replace(':',''))
            tmp_datetime = tmp_date * 10000 + tmp_minute
            for field_name in fields:
                if field_name not in retdict:
                    retdict[field_name] = {}
                field_val = record[field_name]
                if tmp_code not in retdict[field_name]:
                    retdict[field_name][tmp_code] = {}
                if tmp_datetime not in retdict[field_name][tmp_code]:
                    retdict[field_name][tmp_code][tmp_datetime] = {}
                retdict[field_name][tmp_code][tmp_datetime] = field_val
        return retdict
    else:
        df = pd.DataFrame(records)
        df = df.rename(columns={DB_INSTRUMENT_ID: FEATURE_INSTRUMENT_ID})
        # df[FEATURE_DATETIME]=df[DB_DATE]*10000+df[DB_MINUTE]
        return df


def get_stock_return(instrument_ids, start_time, end_time):
    """
    get the return data for stocks in timerange
    :param instrument_ids:
    :param start_time:
    :param end_time:
    :return:
    """
    data = getData(DAY_COLLECTION, instrument_ids, get_calendar(time_shift(start_time, 1), end_time), ['close'])
    df = pd.DataFrame(data['close'])
    df = (df / df.shift(1)).iloc[1:] - 1
    df = df.reindex(get_calendar(start_time, end_time))
    return df.fillna(0)


def get_fundamental_data(instrument_ids, start_time, end_time, fields, collection, return_df=True):
    # TODO:check global conn valid
    StockCodeList = list(instrument_ids)
    dayRange = get_calendar(time_shift(start_time, SHIFT_NUM), end_time)  # 因为基本面数据可能在非交易日公布，所以这里不可以这么写
    start_time_shifted = time_shift(start_time, SHIFT_NUM)
    fields = list(fields)
    true_fields = [1] * len(fields)
    projection_fields = dict(zip(fields, true_fields))
    projection_fields[DB_INSTRUMENT_ID_FUNDAMENTAL] = 1
    projection_fields[DB_DATE] = 1
    projection_fields['_id'] = 0
    records = collection.find(
        {DB_INSTRUMENT_ID_FUNDAMENTAL: {'$in': StockCodeList}, DB_DATE: {'$lt': end_time, '$gte': start_time_shifted}},
        projection_fields)
    records = list(records)
    #############make shape all the same
    if not return_df:
        retdict = dcxdict()
        for field in fields:
            retdict[field] = {}
            for code in StockCodeList:
                retdict[field][code] = {}
                for day in dayRange:
                    retdict[field][code][day] = None

        for record in records:
            tmp_code = record[DB_INSTRUMENT_ID_FUNDAMENTAL]
            tmp_date = record[DB_DATE]
            for field_name in fields:
                if field_name not in retdict:
                    retdict[field_name] = {}
                field_val = record[field_name]
                if tmp_code not in retdict[field_name]:
                    retdict[field_name][tmp_code] = {}
                retdict[field_name][tmp_code][tmp_date] = field_val
        return retdict
    else:
        df = pd.DataFrame(records)
        df = df.rename(columns={DB_INSTRUMENT_ID_FUNDAMENTAL: FEATURE_INSTRUMENT_ID})
        return df


def get_balance_sheet_data(instrument_ids, start_time, end_time, fields, return_df=True):
    return get_fundamental_data(instrument_ids, start_time, end_time, fields, BALANCE_SHEET_COLLECTION, return_df)


def get_profit_sheet_data(instrument_ids, start_time, end_time, fields, return_df=True):
    return get_fundamental_data(instrument_ids, start_time, end_time, fields, PROFIT_SHEET_COLLECTION, return_df)


def get_cashflow_sheet_data(instrument_ids, start_time, end_time, fields, return_df=True):
    return get_fundamental_data(instrument_ids, start_time, end_time, fields, CASHFLOW_SHEET_COLLECTION, return_df)


def get_financial_indicator_sheet_data(instrument_ids, start_time, end_time, fields, return_df=True):
    return get_fundamental_data(instrument_ids, start_time, end_time, fields, FINANCIAL_INDICATOR_COLLECTION, return_df)


if __name__ == '__main__':
    from mongoapi.get_data import get_day_trade_data, get_minute_trade_data
    from feature.time import TimeRange
    from feature import *
    import time
    from mongoapi.config import *

    StockCodeList = ['CN_STK_SH600233', 'CN_STK_SH600104']
    pd.DataFrame(
        get_fundamental_data(StockCodeList, 20110101, 20170901, ['F006N'], BALANCE_SHEET_COLLECTION, return_df=False)[
            'F006N']).fillna(method='ffill').loc[20110101:20170901]
    fields = ['close', 'volume']
    dayRange = get_calendar(20130501, 20170531)
    # set collection
    conn = pymongo.MongoClient('localhost', MONGODB_PORT)
    db = conn[MONGODB_DB]
    col = db[MONGODB_COLLECTION_DAY]
    #
    print('test $in get data')
    start_time = time.time()
    tmpdata = getData(col, StockCodeList, dayRange, fields)
    end_time = time.time()
    print('used time: %d' % (end_time - start_time))

    #
    print('test $gt $lt get data')
    start_time = time.time()
    tmpdata = getData_V2(col, StockCodeList, 20130501, 20170531, fields)
    end_time = time.time()
    print('used time: %d' % (end_time - start_time))

    # ret_day = get_day_trade_data(c, TimeRange(20130501, 20170531), fields)
    # ret_minute = get_minute_trade_data(c, TimeRange(20170501, 20170531), fields)
    # import pandas as pd
    #
    # pd.DataFrame(ret_minute['close']['CN_STK_SH600233'])
    # print(ret_day)
    # print(ret_minute)
