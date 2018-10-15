# -*- coding: utf-8 -*-
from quantlab_utils.utils import time_shift
class TimeRange(object):
    """Time range with freq."""

    # '2017-1'-'2017-5' means from 2017.1.1 0:0:0 to 2017-5-31 23:59:59
    # '2012' - '2017' means from 2012.1.1 to 2017.12.31
    def __init__(self, begin, end, freq='1d'):
        self.begin_time = begin
        self.end_time = end
        self.freq = freq

    def __str__(self):
        return 'TimeRange(begin_time={}, end_time={}, freq={})'.format(
            self.begin_time, self.end_time, self.freq)

    def __repr__(self):
        return str(self)

    def shift(self,period):
        if period>0:
            return TimeRange(time_shift(self.begin_time,period),self.end_time)
        elif period<0:
            return TimeRange(self.begin_time,time_shift(self.end_time,period))
