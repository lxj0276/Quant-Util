# -*- coding: utf-8 -*-
import ast
import glob
import os

import imp
import numpy as np
import pandas as pd
import xarray as xr
from feature.SubmitFeature import SubmitFeature
from feature.config import set_option
from feature.env import *
from feature.load_struct import features_dict
from redis_cache.rediscache import cache_it_pickle


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
            getattr(imp.reload(__import__('feature', fromlist=[fname.split('.')[0]])), x)
            for x in classes
        ]
    features = list(filter(lambda x: x.description.lower().find(keyword.lower()) != -1, features))
    return features


@cache_it_pickle(expire=60 * 60)
def load_dataset(instrument_ids, features, time_range, skip_suspend=False, skip_na=True, expand=False,
                 return_xarray=False):
    # TODO: check feature granularity

    # set global option
    set_option('skip_suspend', skip_suspend)
    # set_calendar(calendar_type)
    dataset = features_dict()
    for feature in features:
        dataset[feature.get_name()] = feature.load(instrument_ids, time_range)

    if return_xarray:
        data = np.stack(dataset.values(), axis=-1)
        features = list(dataset.keys())
        df = dataset[features[0]]
        coords = {'datetime': df.index, 'instrument_id': df.columns, 'feature': features}
        dims = ['datetime', 'instrument_id', 'feature']
        dataset = xr.DataArray(data, dims=dims, coords=coords)
        return dataset
    else:
        dataset = dataset.to_DataFrame()
        if expand:
            dataset = dataset.pivot(columns='instrument_id')

        if skip_na:
            dataset = dataset.replace([np.inf, -np.inf], np.nan)
            dataset = dataset.dropna()
    return dataset


def load_dataset_nocache(instrument_ids, features, time_range, skip_suspend=False, skip_na=True, expand=False,
                         return_xarray=False):
    # TODO: check feature granularity

    # set global option
    set_option('skip_suspend', skip_suspend)
    # set_calendar(calendar_type)
    dataset = features_dict()
    for feature in features:
        dataset[feature.get_name()] = feature.load(instrument_ids, time_range)

    if return_xarray:
        data = np.stack(dataset.values(), axis=-1)
        features = list(dataset.keys())
        df = dataset[features[0]]
        coords = {'datetime': df.index, 'instrument_id': df.columns, 'feature': features}
        dims = ['datetime', 'instrument_id', 'feature']
        dataset = xr.DataArray(data, dims=dims, coords=coords)
        return dataset
    else:
        dataset = dataset.to_DataFrame()
        if expand:
            dataset = dataset.pivot(columns='instrument_id')

        if skip_na:
            dataset = dataset.replace([np.inf, -np.inf], np.nan)
            dataset = dataset.dropna()
    return dataset


def submit_feature(filename, data=dict()):
    submitFeature = SubmitFeature(filename, data)
    submitFeature.submitFeature()
