# -*- coding: utf-8 -*-
import copy
import numpy as np
import pandas as pd


class Dataset(object):
    """数据接口"""
    def __init__(self, datetime=[], instrument_id=[], feature=[], pct_change=[], feature_names=None, freq='1d'):
        try:
            assert len(datetime) == len(instrument_id) == len(feature) == len(pct_change)
        except:
            raise ValueError('all arguments must have equal length')
        self._datetime = np.array(datetime, dtype=np.datetime64)
        self._instrument_id = np.array(instrument_id)
        self._feature = np.array(feature)
        self._pct_change = np.array(pct_change)
        self._label  = np.where(pct_change>0, 1, 0)
        self._weight  = np.abs(pct_change)
        self._feature_names = np.array(feature_names) if feature_names is not None else np.array(['f%d'%x for x in range(self._feature.shape[1])])
        self._freq = freq
    
    @property
    def feature(self):
        return self._feature

    @property
    def feature_names(self):
        return self._feature_names
    
    @property
    def label(self):
        return self._label
    
    @property
    def weight(self):
        return self._weight
    
    @property
    def datetime(self):
        return self._datetime
    
    @property
    def instrument_id(self):
        return self._instrument_id
    
    @property
    def pct_change(self):
        return self._pct_change

    @property
    def freq(self):
        return self._freq
    
    def copy(self):
        return copy.copy(self)
    
    def slice(self, index):
        return Dataset(
            datetime=self.datetime[index], 
            instrument_id=self.instrument_id[index], 
            feature=self.feature[index],
            pct_change=self.pct_change[index],
            feature_names=self.feature_names,
            freq=self.freq,
        )
    
    def slice_by_datetime(self, begin_time, end_time, keep=True):
        begin_time = np.datetime64(begin_time)
        end_time = np.datetime64(end_time)
        index = (self._datetime >= begin_time) & (self._datetime < end_time)
        if not keep: index = ~index
        return self.slice(index)
    
    def slice_by_instrument_id(self, instrument_id, keep=True):
        instrument_id = set(instrument_id)
        index = np.array([x in instrument_id for x in self.instrument_id])
        if not keep: index = ~index
        return self.slice(index)
    
    def as_frame(self):
        df = pd.DataFrame(self.feature, index=self.datetime, columns=self.feature_names)
        df['pct_change'] = self.pct_change
        df['label'] = self.label
        df['weight'] = self.weight
        df.insert(0, 'instrument_id', self.instrument_id)
        return df
