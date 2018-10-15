import pandas as pd
from .data import Dataset


# 滚动窗口
def train_test_split(dataset, train_span=48, valid_span=3, test_span=3, unit='M'):
    """将数据按照滑动时间窗口切分
    `unit=D`为按照日的滑动
    `unit=W`为按照周的滑动
    `unit=M`为按照月的滑动
    `unit=Y`为按照年的滑动
    """
    try:
        assert isinstance(dataset, Dataset)
    except:
        raise ValueError('dataset should be a Dataset instance')
    begin_time = pd.to_datetime(min(dataset.datetime))
    end_time   = pd.to_datetime(max(dataset.datetime) + 1)
    unit_mapping = {
        'D': 'days',
        'W': 'weeks',
        'M': 'months',
        'Y': 'years',
    }
    unit = unit.upper()
    if unit not in unit_mapping:
        raise ValueError('unit {} is not valid, possible values are {}'.format(
            unit, ', '.join(unit_mapping.keys())
        ))
    test_time  = begin_time + pd.DateOffset(**{unit_mapping[unit]: train_span + valid_span + test_span})
    if test_time > end_time:
        raise ValueError('train({})+valid({})+test({}) exceed maximum time range {:%Y/%m/%d}~{:%Y/%m/%d}'.format(
            train_span, valid_span, test_span, begin_time, end_time
        ))
    while test_time < end_time:
        train_time = begin_time + pd.DateOffset(**{unit_mapping[unit]: train_span})
        valid_time = train_time + pd.DateOffset(**{unit_mapping[unit]: valid_span})
        test_time  = valid_time + pd.DateOffset(**{unit_mapping[unit]:  test_span})
        dtrain = dataset.slice_by_datetime(begin_time, train_time)
        dvalid = dataset.slice_by_datetime(train_time, valid_time)
        dtest  = dataset.slice_by_datetime(valid_time, test_time)
        yield dtrain, dvalid, dtest
        begin_time += pd.DateOffset(**{unit_mapping[unit]: valid_span or test_span})
    
def format_datetime64(datetime):
    return str(datetime).split('T')[0]
