# -*- coding: utf-8 -*-
import pickle
import itertools
import numpy as np
import xgboost as xgb


# 策略模型
class Model(object):
    """策略模型
    - 基于xgboost.Booster二分类模型
    - 自动记录最优训练轮数
    """
    def __init__(self, param, n_estimators=10):
        self._param  = param
        self._n_estimators = n_estimators
        self._best_nround = 0
        
    def __str__(self):
        return 'Model(n_estimators=%d, ' % self._n_estimators + \
            ', '.join(key+'='+str(value) for key, value in self._param.items()) + \
            ')'

    def __repr__(self):
        return str(self)
        
    def _normalize(self, x):
        if not self._fitted:
            self._mean = np.mean(x, axis=0)
            self._std  = np.std(x, axis=0)
        x = (x - self._mean) / self._std
        return x
        
    def boost(self):
        for m in self._model:
            m.update(self._dtrain, self._iteration)
        self._iteration += 1
        self._fitted = True

    def optimize(self, nround=10, scorer=None):
        best_score = -np.inf
        best_nround = 0
        for r in range(nround):
            self.boost()
            if scorer is None:
                continue
            score = scorer(self)
            if score > best_score:
                best_score  = score
                best_nround = r+1
        self._best_nround = best_nround
        return best_score
        
    def init(self, x, y, sample_weight=None):
        self._fitted = False
        self._iteration  = 0
        x = self._normalize(x)
        self._dtrain = xgb.DMatrix(x, label=y, weight=sample_weight)
        self._model  = [
            xgb.Booster(dict(seed=i, **self._param), [self._dtrain])
            for i in range(self._n_estimators)
        ]
            
    def predict(self, x):
        if not self._fitted:
            raise RuntimeError('model is not trained yet!')
        x = self._normalize(x)
        data = xgb.DMatrix(x)
        scores = np.zeros(len(x))
        for m in self._model:
            scores += m.predict(data, ntree_limit=self._best_nround)
        scores /= self._n_estimators
        return scores
    

_DEFAULT_PARAM_GRID = {
    'objective': ['binary:logistic'], 
    'nthread': [10], 
    'max_depth': [4, 5, 6],
    'colsample_bytree': [0.3, 0.4, 0.6, 0.8],
    'subsample': [0.6, 0.8],
}
def model_train(dtrain, scorer=None, param_grid=None):
    """train model based with grid search and certain scorer."""

    # check param
    if param_grid is None:
        param_grid = _DEFAULT_PARAM_GRID
        
    # data prepare
    x_train = dtrain.feature
    y_train = dtrain.label
    sample_weight = dtrain.weight

    ## parameter tunning
    print('* Step #1: model parameter tunning')
    nround = 50
    param = {'learning_rate': 0.3}
    keys = param_grid.keys()
    best_score = -np.inf
    best_param = dict()
    for values in itertools.product(*[param_grid[k] for k in keys]):
        # create param
        param.update(**dict(zip(keys, values)))
        # model training
        model = Model(param)
        model.init(x_train, y_train, sample_weight)
        _best_score = model.optimize(nround, scorer)
        if _best_score > best_score:
            best_score = _best_score
            best_param = param
            
    print('best param:', best_param)

    ## nround tunning
    print('* Step #2: model fine tunning')
    best_param['learning_rate'] = 0.1
    nround = 300
    model  = Model(best_param)
    model.init(x_train, y_train, sample_weight)
    model.optimize(nround, scorer)
    
    return model


def save_model(model, fname):
    try:
        assert isinstance(model, Model)
    except:
        raise TypeError('only Model instance is accepted')

    if not model._fitted:
        raise ValueError('model is not fitted yet!')
    
    obj = dict()
    obj['model'] = model._model
    obj['param'] = model._param
    obj['n_estimators'] = model._n_estimators
    obj['mean']  = model._mean
    obj['std']   = model._std
    obj['best_nround'] = model._best_nround
    with open(fname, 'wb') as f:
        pickle.dump(obj, f)
    print('note: the saved model can only be used for predict.')

    
def load_model(fname):
    with open(fname, 'rb') as f:
        obj = pickle.load(f)
    model = Model(obj['param'], n_estimators=obj['n_estimators'])
    model._model = obj['model']
    model._fitted = True
    model._mean = obj['mean']
    model._std  = obj['std']
    model._best_nround = obj['best_nround']
    print('note: this model can only be used for predict.')
    return model
