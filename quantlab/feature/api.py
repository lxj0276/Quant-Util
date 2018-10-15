# -*- coding: utf-8 -*-
import os
import ast
import imp
import glob
import multiprocess
import numpy as np
import pandas as pd
from .env import *
from .utils import pickle_load, pickle_dump, hash_args
from .cache import mem_cache
from .config import set_option, set_calendar
from .SubmitFeature import SubmitFeature


def list_instrument_ids(country='*', instrument_type='*'):
    """list all instrument_ids."""
    instrument_ids = []
    for fname in glob.glob(os.path.join(INSTRUMENT_ID_PATH, '{}_{}.csv'.format(country, instrument_type))):
        with open(fname) as f:
            instrument_ids += [x.strip() for x in f]
    return sorted(instrument_ids)


def list_features(keyword=''):
    """list all features, can filter features by keyword."""
    features = []
    lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zoo')
    for fname in os.listdir(lib_path):
        if fname[:2] == '__' or fname[-3:] != '.py': continue
        with open(os.path.join(lib_path, fname), 'rb') as f:
            source = f.read()
        classes = [node.name for node in ast.walk(ast.parse(source)) if isinstance(node, ast.ClassDef)]
        features += [
            getattr(imp.reload(__import__('quantlab.feature', fromlist=[fname.split('.')[0]])), x)()
            for x in classes
        ]
    features = filter(lambda x: x.description.lower().find(keyword.lower()) != -1, features)
    return sorted(features)


def load_dataset(instrument_ids, time_range, features, skip_suspend=False, skip_na=True, expand=False, overwrite=False, processes=5, verbose=True, calendar_type='CN_STK'):
    # TODO: check feature granularity

    # set global option
    set_option('skip_suspend', skip_suspend)
    set_calendar(calendar_type)

    load_success_flag = True

    md5 = hash_args(sorted(instrument_ids), sorted(features), skip_suspend=skip_suspend)
    
    fname = os.path.join(CACHE_PATH, md5[:2], md5[2:4], md5)

    # load dataset from cache
    if not overwrite and os.path.exists(fname):
        if verbose:
            print('begin loading existing dataset from cache {}...'.format(md5))
        try:
            dataset = pickle_load(fname)
        except EOFError:
            load_success_flag = False
            print("load {} for whole dataset fail, it will be overwrite".format(fname))
        else:
            if dataset.empty or dataset.index.max().date() < time_range.end_time.date():
                cache_max_date = 'NaT' if dataset.empty else dataset.index.max().date()
                print('end time `{}` exceeds cache max date `{}`, will force update cache...'.format(
                    time_range.end_time.date(), cache_max_date))
                overwrite = True # force update features

    # create new dataset
    if overwrite or not os.path.exists(fname) or not load_success_flag:
        if verbose:
            print('begin creating dataset, it may take some time...')

        if processes > 1:
            try:
                pool = multiprocess.Pool(processes=processes)
                dataset = pool.map(
                    lambda x: load_single_dataset(x, time_range, features, skip_suspend=skip_suspend, overwrite=overwrite),
                    instrument_ids
                )
            finally:
                pool.terminate()
        else:
            dataset = [
                load_single_dataset(x, time_range, features, skip_suspend=skip_suspend, overwrite=overwrite)
                for x in instrument_ids
            ]

        dataset = pd.concat(dataset)
        dataset.index.name = 'datetime'

        if verbose:
            print('begin dumping dataset {}...'.format(md5))

        pickle_dump(dataset, fname)

    # if expand is True, the dataset will have two dimensions: time and instrument id. The value is features[0].
    # if expand is False, the dataset will have two dimensions: time and feature_name. While the first column is instrument_ids
    if expand:
        dataset = dataset.pivot(columns='instrument_id')

    if skip_na:
        dataset = dataset.replace([np.inf, -np.inf], np.nan)
        dataset = dataset.dropna()
        
    if not dataset.empty:
        dataset = dataset[(dataset.index>=time_range.begin_time)&(dataset.index<=time_range.end_time)]

    return dataset


def load_single_dataset(instrument_id, time_range, features, skip_suspend=False, overwrite=False):
    tmp = []
    for feature in features:
        if DEBUG:
            print(feature, instrument_id)
        load_success_flag = False
        md5 = hash_args(instrument_id, feature, skip_suspend=skip_suspend)
        fname = os.path.join(CACHE_PATH, md5[:2], md5[2:4], md5)
        try:
            if not overwrite and os.path.exists(fname):
                try:
                    series = pickle_load(fname)
                except EOFError:
                    print("load {} for {} fail, it will be overwrite".format(fname, str(feature)))
                else:
                    if not series.empty and series.index.max().date() >= time_range.end_time.date():
                        load_success_flag = True
            if not load_success_flag:
                series = feature.load(instrument_id, time_range) # WILL DEPRECATED: keep time_range for compatibility
                pickle_dump(series, fname)
            tmp.append(series)
        except Exception as e:
            print('feature exception: {} {} {}'.format(instrument_id, feature, e))
            raise
    tmp = pd.concat(tmp, axis=1, join='outer') #TODO: inner/outer join
    tmp.insert(0, 'instrument_id', pd.Series(instrument_id, index=tmp.index))
    return tmp


def submit_feature(filename, data=dict()):
    submitFeature = SubmitFeature(filename, data)
    submitFeature.submitFeature()
