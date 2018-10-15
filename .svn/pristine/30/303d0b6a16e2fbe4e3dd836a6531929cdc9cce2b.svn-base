# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


def train_valid_test_split(dataset, features, labels, split=0.6):
    """ split dataset into train/valid/test set.

    Parameters
    ----------
    dataset  : original dataset with date as dataframe
    features : feature column names
    labels   : label column names
    split    : percentage for train, valid and test will share 1-split

    Returns
    ----------
    (x_train, y_train, i_train, x_valid, y_valid, i_valid, x_test, y_test, i_test)
    """
    indexes   = sorted(dataset.index.unique())
    n_index   = len(indexes)
    train_loc = indexes[int(n_index*split)]
    valid_loc = indexes[int(n_index*(split+1)*0.5)]

    i_train = dataset.index.map(lambda x: x<train_loc).values
    i_valid = dataset.index.map(lambda x: train_loc<=x<valid_loc).values
    i_test  = dataset.index.map(lambda x: x>=valid_loc).values

    x_train = dataset.loc[i_train, features].as_matrix()
    y_train = dataset.loc[i_train, labels].as_matrix()
    
    x_valid = dataset.loc[i_valid, features].as_matrix()
    y_valid = dataset.loc[i_valid, labels].values
    
    x_test  = dataset.loc[i_test, features].as_matrix()
    y_test  = dataset.loc[i_test, labels].values
    
    print('train:', '%s~%s'%(dataset[i_train].index[0], dataset[i_train].index[-1]), ',', x_train.shape[0], 'samples')
    print('valid:', '%s~%s'%(dataset[i_valid].index[0], dataset[i_valid].index[-1]), ',', x_valid.shape[0], 'samples')
    print('test:', '%s~%s'%(dataset[i_test].index[0], dataset[i_test].index[-1]), ',', x_test.shape[0], 'samples')

    return x_train, y_train, i_train, x_valid, y_valid, i_valid, x_test, y_test, i_test
