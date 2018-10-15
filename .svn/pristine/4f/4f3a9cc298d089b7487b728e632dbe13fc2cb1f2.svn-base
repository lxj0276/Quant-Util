# -*- coding: utf-8 -*-
import os
import pandas as pd
from abc import ABC, abstractmethod
from .env import *
from .utils import pickle_load, pickle_dump, find_date_index, hash_args, freq_resample
from .error import OriginalFeatureError, PersistentFeatureError
from .cache import mem_cache
from .config import get_option, get_calendar


class InstrumentIDRelated(object):
    """Instrument_id related feature."""

    def _get_path(self, instrument_id, feature_name, feature_version):
        folder = (instrument_id + '.' + feature_name.upper())
        md5    = hash_args(folder)[:FEATURE_HASH_LEN]
        return os.path.join(FEATURE_PATH, md5, folder, feature_version+'.pkl')


class InstrumentIDUnRelated(object):
    """Instrument_id unrelated feature."""

    def _get_path(self, instrument_id, feature_name, feature_version):
        folder = feature_name.upper()
        md5    = hash_args(folder)[:FEATURE_HASH_LEN]
        return os.path.join(FEATURE_PATH, md5, folder, feature_version+'.pkl')


class Feature(InstrumentIDRelated, ABC):
    """Feature base class."""

    description = 'feature base class'

    granularity = 'day' # or 'minute'

    @property
    def _classname(self):
        return type(self).__name__

    @property
    def name(self):
        if '__' in self._classname:
            return ''.join(self._classname.split('__')[:-1])
        return self._classname
    
    @property
    def version(self):
        if '__' in self._classname:
            return self._classname.split('__')[-1]
        return 'latest'

    def __str__(self):
        return self.name

    def __repr__(self):
        return '{}(version=\'{}\', granularity=\'{}\', description=\'{}\')'.format(
            self.name, self.version, self.granularity, self.description)

    def __lt__(self, other):
        return str(self) < str(other)

    def load(self, instrument_id, time_range):
        # get global option
        skip_suspend = get_option('skip_suspend', False)

        md5 = hash_args(str(self), instrument_id, skip_suspend=skip_suspend)

        # check cache
        if md5 in mem_cache:
            if DEBUG:
                print(self.name, instrument_id, 'hit mem_cache', md5)
            return mem_cache[md5]

        # load
        series = self._load_feature(instrument_id, time_range)
        series.name = str(self)

        # handle suspend period
        if skip_suspend:
            series = series.dropna()

        # cache
        mem_cache[md5] = series

        return series
        
    @abstractmethod
    def _load_feature(self, instrument_id, time_range):
        # time_range will be removed in the future
        pass

    @abstractmethod
    def _create_feature(self, instrument_id, time_range):
        # time_range will be removed in the future
        pass


class PersistentFeature(Feature):
    """persistent feature."""

    def _load_feature(self, instrument_id, time_range):

        # load feature
        fname = self._get_path(instrument_id, self.name, self.version)
        series = pd.Series()
        if os.path.exists(fname):
            if DEBUG:
                print(self.name, instrument_id, 'load from', fname)
            series = pickle_load(fname)
            series = series[~series.index.duplicated(keep='last')] 
        # # compatible with old api
        # elif os.path.exists(fname.rstrip('.pkl')):
        #     import glob
        #     for f in sorted(glob.glob(fname.replace('.pkl', '/*.pkl'))):
        #         series = pd.concat([series, pickle_load(f)])
        #     series = series[~series.index.duplicated(keep='last')]
        #     pickle_dump(series, fname)
            
        # check datetime
        if series.empty or series.index.max().date() < time_range.end_time.date():
            if DEBUG:
                print(self.name, instrument_id, 'create feature')
            try:
                extra_series = self._create_feature(instrument_id, time_range)
                series = pd.concat([series, extra_series])
                series = series[~series.index.duplicated(keep='last')]
                pickle_dump(series, fname)
            except OriginalFeatureError:
                pass
            
        return series

    
class NonPersistentFeature(Feature):
    """non-persistent feature."""

    def _load_feature(self, instrument_id, time_range):
        return self._create_feature(instrument_id, time_range)


class OperatorFeature(Feature):
    """operator feature."""

    def __repr__(self):
        return str(self)
    
    def _create_feature(self, instrument_id, time_range):
        raise OperatorFeatureCreateError
