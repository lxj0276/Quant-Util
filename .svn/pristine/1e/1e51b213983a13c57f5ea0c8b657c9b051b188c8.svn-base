# -*- coding: utf-8 -*-
import os
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
from feature.config import get_option
from feature.env import *
from feature.error import OriginalFeatureError
from feature.mongowrap import load_single_feature_from_mongo_df, load_is_original
from feature.utils import hash_args
from feature.time import TimeRange
from mongoapi.utils import cxdict_2_df
from redis_cache.rediscache import cache_it_pickle,cache_it_timeseries


class InstrumentIDRelated(object):
    """Instrument_id related feature."""

    def _get_path(self, instrument_id, feature_name, feature_version):
        folder = (instrument_id + '.' + feature_name.upper())
        md5 = hash_args(folder)[:FEATURE_HASH_LEN]
        return os.path.join(FEATURE_PATH, md5, folder, feature_version + '.pkl')


class InstrumentIDUnRelated(object):
    """Instrument_id unrelated feature."""

    def _get_path(self, instrument_id, feature_name, feature_version):
        folder = feature_name.upper()
        md5 = hash_args(folder)[:FEATURE_HASH_LEN]
        return os.path.join(FEATURE_PATH, md5, folder, feature_version + '.pkl')


class Feature(InstrumentIDRelated, ABC):
    """Feature base class."""

    description = 'feature base class'

    granularity = 'day'  # or 'minute'

    @property
    def _classname(self):
        return type(self).__name__

    def set_name(self, name):
        self.short_name = name
        return self

    def get_name(self):
        if hasattr(self, 'short_name'):
            return self.short_name
        else:
            return str(self)

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

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '{}(version=\'{}\', granularity=\'{}\', description=\'{}\')'.format(
            self.name, self.version, self.granularity, self.description)

    def __lt__(self, other):
        return str(self) < str(other)

    def load(self, instrument_ids, time_range):
        # get global option
        skip_suspend = get_option('skip_suspend', False)
        series = self._load_feature(instrument_ids, time_range)
        for instrument_id in instrument_ids:
            if instrument_id not in series.columns:
                series[instrument_id] = np.nan
        series = series[instrument_ids].astype(np.float64)  # 这里使用astype是因为填充的nan会导致该列为object类型
        setattr(series, '__name', str(self))
        if skip_suspend:
            series = series.dropna()

        return series

    @abstractmethod
    def _load_feature(self, instrument_id, time_range):
        # time_range will be removed in the future
        pass

    @abstractmethod
    def _create_feature(self, instrument_id, time_range):
        # time_range will be removed in the future
        pass

    def __hash__(self):
        return self.__str__()


class PersistentFeature(Feature):
    """persistent feature."""
    #
    # @cache_it_pickle(60 * 60 * 12)
    # def _load_feature(self, instrument_ids, time_range):
    #     series = pd.Series()
    #     if load_is_original(str(self)):
    #         #############name to hash the function caller
    #         series = self.__load_feature(instrument_ids, time_range)
    #     else:
    #         if DEBUG:
    #             print(self.name, instrument_ids, 'create feature')
    #         try:
    #             series = self._create_feature(instrument_ids, time_range)
    #             series = series[~series.index.duplicated(keep='last')]
    #         except OriginalFeatureError:
    #             pass
    #             #######################cat theseries
    #     # if not series.empty:
    #     #     series = series[(series.index>=time_range.begin_time)&(series.index<=time_range.end_time)]
    #     return series


    def _load_feature(self, instrument_ids, time_range):
        return self.__timeseries_cache_load(instrument_ids,start_time=time_range.begin_time,end_time=time_range.end_time)

    @cache_it_timeseries(60*60*24)
    def __timeseries_cache_load(self,instrument_ids,start_time,end_time):
        time_range=TimeRange(start_time,end_time)
        series = pd.Series()
        if load_is_original(str(self)):
            #############name to hash the function caller
            series = self.__load_feature(instrument_ids, time_range)
        else:
            if DEBUG:
                print(self.name, instrument_ids, 'create feature')
            try:
                series = self._create_feature(instrument_ids, time_range)
                series = series[~series.index.duplicated(keep='last')]
            except OriginalFeatureError:
                pass
                #######################cat theseries
        # if not series.empty:
        #     series = series[(series.index>=time_range.begin_time)&(series.index<=time_range.end_time)]
        return series

    def __load_feature(self, instrument_ids, time_range):
        df = load_single_feature_from_mongo_df(instrument_ids, str(self), start_time=time_range.begin_time,
                                               end_time=time_range.end_time)
        # df=df.sort_index(ascending=True)
        return df


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
