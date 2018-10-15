from abc import abstractmethod, ABC

import numpy as np
import pandas as pd
from feature.ops import Ranking
from feature.api import load_dataset
from numpy.lib.nanfunctions import nanmean, nanstd, nansum, nanmax, nanmin
from mongoapi.config import DB_DATETIME

class Feature_Analyse(ABC):
    description = 'feature base class'

    granularity = 'day'  # or 'minute'

    def __init__(self):
        pass

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

    @property
    def _classname(self):
        return type(self).__name__

    def __str__(self):
        return self.name

    def load(self, instrument_ids, time_range):
        return self._load(instrument_ids=instrument_ids, time_range=time_range)

    @abstractmethod
    def _load(self, instrument_ids, time_range):
        pass

    def __repr__(self):
        return '{}(version=\'{}\', granularity=\'{}\', description=\'{}\')'.format(
            self.name, self.version, self.granularity, self.description)


class Corr(Feature_Analyse):
    description = "两个feature的相关系数"

    def __init__(self, feature_left, feature_right):
        self.feature_left = feature_left
        self.feature_right = feature_right
        super(Corr, self).__init__()

    def _load(self, instrument_ids, time_range):
        feature_left = self.feature_left.load(instrument_ids, time_range)
        feature_right = self.feature_right.load(instrument_ids, time_range)
        feature_left = feature_left.values.reshape((-1,))
        feature_right = feature_right.values.reshape((-1,))
        not_nan_idx = (~np.isnan(feature_left)) & (~np.isnan(feature_right))

        return np.corrcoef(feature_left[not_nan_idx], feature_right[not_nan_idx])[0, 1]


class Corr_With_Return(Corr):
    description = "某个feature和接下来N天收益的相关系数"

    def __init__(self, feature, return_delay_days):
        from feature.zoo.Return_Daily import Return_NDay
        feature_left = feature
        feature_right = Return_NDay(return_delay_days)
        super(Corr_With_Return, self).__init__(feature_left, feature_right)


class Corr_With_NextDay_Return(Corr_With_Return):
    description = "某个feature和接下来一天的收益相关系数"

    def __init__(self, feature):
        super(Corr_With_NextDay_Return, self).__init__(feature, 1)


class Feature_Importance_Base(Feature_Analyse):
    description = "计算一系列feature 的feature importance,(via time)"

    def __init__(self, analyse_features, target_feature):
        self.analyse_features = analyse_features
        self.target_feature = target_feature
        self.analyse_feature_names = list(map(lambda x: x.get_name(), self.analyse_features))
        super(Feature_Importance_Base, self).__init__()

    def _load(self, instrument_ids, time_range):
        from xgboost.sklearn import XGBClassifier, XGBRegressor
        from feature.api import load_dataset
        dataset = load_dataset(instrument_ids, self.analyse_features + [self.target_feature], time_range,
                               return_xarray=False).reset_index()
        clf = XGBClassifier()
        clf.fit(dataset[['datetime'] + self.analyse_feature_names], dataset[self.target_feature.get_name()])
        importances = pd.Series(clf.feature_importances_, index=['datetime'] + self.analyse_feature_names)
        return importances


class Feature_Importance_Nday(Feature_Importance_Base):
    description = "计算一系列feature 的feature importance，与接下来的N天收益率对比 default N=1"

    def __init__(self, analyse_features, N=1):
        from feature.zoo.Return_Daily import Return_NDay_Label
        target_feature = Return_NDay_Label(N)
        super(Feature_Importance_Nday, self).__init__(analyse_features, target_feature)


class Feature_Statistic(Feature_Analyse):
    description = '基础的feature 统计特征，base类型'

    def __init__(self, feature):
        self.feature = feature
        super(Feature_Statistic, self).__init__()


class Feature_Std(Feature_Statistic):
    description = "因子标准差，按股票平均"

    def _load(self, instrument_ids, time_range):
        feature = self.feature.load(instrument_ids, time_range)
        return nanmean(nanstd(feature, axis=0))


class Feature_Ranking_Std(Feature_Statistic):
    description = "因子排序标准差，按股票平均"

    def _load(self, instrument_ids, time_range):
        feature = Ranking(self.feature).load(instrument_ids, time_range)
        return nanmean(nanstd(feature, axis=0))


class Feature_Score(Feature_Analyse):
    """
    因子的inplace permutation，如果值较大，说明因子具有明显的解释作用
    """
    def __init__(self,feature,N=1):
        self.feature=feature
        from feature.zoo.Return_Daily import Return_NDay_Label
        self.target_feature = Return_NDay_Label(N)
        super(Feature_Score,self).__init__()

    def _load(self, instrument_ids, time_range):
        results=[self.__load(instrument_ids, time_range) for x in range(20)]
        return sum(results)/len(results)

    def __load(self, instrument_ids, time_range):
        # from xgboost.sklearn import XGBClassifier, XGBRegressor
        # from feature.api import load_dataset
        from xgboost.sklearn import  XGBClassifier
        from sklearn.model_selection import train_test_split

        #---------------------CHOOSE ONE HERE
        dataset = load_dataset(instrument_ids,
                               [self.feature,self.target_feature],
                               time_range,
                               return_xarray=False).reset_index()
        X = dataset[[DB_DATETIME, self.feature.get_name()]].values
        y = dataset[self.target_feature.get_name()].values

        #-----------------------------------------------------------------
        clf = XGBClassifier(max_depth=4, n_estimators=400, learning_rate=0.05)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)
        eval_set = [(X_test, y_test)]
        clf.fit(X_train,y_train,eval_set=eval_set,early_stopping_rounds=10)
        Score_Origin=clf.score(X_test,y_test)
        #--------------------------------------------------------------------
        clf = XGBClassifier(max_depth=4, n_estimators=400, learning_rate=0.05)
        X_Permuted=X.copy()
        np.random.shuffle(X_Permuted[:,1])
        X_Permuted_train, X_Permuted_test, y_train, y_test = train_test_split(X_Permuted, y, test_size=0.2, random_state=7)
        eval_set = [(X_Permuted_test, y_test)]
        clf.fit(X_Permuted_train,y_train,eval_set=eval_set,early_stopping_rounds=10)
        Score_Permuted=clf.score(X_Permuted_test,y_test)
        return Score_Origin-Score_Permuted


class Feature_Stablize(Feature_Analyse):

    def __init__(self, feature, N=1):
        self.feature = feature
        from feature.zoo.Return_Daily import Return_NDay_Label
        self.target_feature = Return_NDay_Label(N)
        super(Feature_Score, self).__init__()

    def __load(self, instrument_ids, time_range):
        # from xgboost.sklearn import XGBClassifier, XGBRegressor
        # from feature.api import load_dataset
        from sklearn.ensemble import RandomForestClassifier
        clf = RandomForestClassifier(max_depth=4, n_estimators=200)
        # ---------------------CHOOSE ONE HERE--------------------
        dataset = load_dataset(instrument_ids,
                               [self.feature, self.target_feature],
                               time_range,
                               return_xarray=False).reset_index()

        X = dataset[[DB_DATETIME, self.feature.get_name()]].values
        y = dataset[self.target_feature.get_name()].values





