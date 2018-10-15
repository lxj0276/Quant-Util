import pandas as pd
import numpy as np
import xgboost as xgb
import cufflinks as cf
from quantlab.feature import *
from quantlab.feature.ops import *

import plotly as py
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot, plot

def process_single_day(df, feature_name, n=5):
    if not feature_name in df.columns.values:
        raise IndexError('no {} in features'.format(feature_name))
    if not 'pct_change' in df.columns.values:
        raise IndexError('no pct_change in features')
    group = np.array_split(df.sort_values(feature_name,ascending=False),n)
    return pd.Series([np.mean(i['pct_change']) for i in group])

def monotonous(df):
    '''
    elements in df should be iterable and have the same length
    '''
    length = len(df)
    pos_mono = np.array(range(len(df.columns)))
    neg_mono = pos_mono[::-1]
    pos_score = 0
    neg_score = 0
    series_list = np.array([list(df[i]) for i in df])
    for i in range(length):
        index_sort = np.argsort(series_list[:,i])
        pos_score += np.sum(np.square(index_sort-pos_mono))
        neg_score += np.sum(np.square(index_sort-neg_mono))
    return min(pos_score, neg_score)/length

def valid_test(dataset, feature_name, notebook_mode=True, showfig=True):
    '''
    Plot the return sorted by feature_name
    feature_name and 'pct_change' must be in dataset.columns
    dataset.index should be pd.Timestamp
    notebook_mode = True if you are using Jupyter notebook
    fig_output = True if you want to visualize the result

    Input:
        dataset -> pd.DataFrame
        feature_name -> str (column you want to test)

    Output:
        dict :
            'return': np.array (return of assets sorted by the feature you test)
            'sharpe': np.array (annual sharpe of assets sorted bu the feature you test)
            'diff_return': float (return of long-short hedge)
            'diff_sharpe': float (annual sharpe of lonng-short hedge)
    '''
    color_list = ['rgb(254,67,101)','rgb(252,157,154)','rgb(249,205,173)',
                  'rgb(200,200,169)','rgb(131,175,155)','rgb(20,68,106)']
    if not 'limit' in dataset:
        raise ValueError(' dataset should have column \'limit\', which is today\'s pct_change. When it is larger than 0.098, we regard it reach the limit_up and can not be bought')
    dataset = dataset[dataset['limit']<0.098]
    return_series = dataset.groupby(dataset.index).apply(lambda x:process_single_day(x,feature_name))
    return_series_list = [np.exp(np.cumsum(np.log1p(return_series[column]))) for column in return_series]

    diff_return = return_series.iloc[:,0]-return_series.iloc[:,-1]
    diff_return_list = np.exp(np.cumsum(np.log1p(diff_return)))
    duration = (max(dataset.index)-min(dataset.index)).days/365
    annual_diff_return = (np.power(diff_return_list[-1],1/duration)-1)*100
    annual_return_list = [(np.power(i[-1],1/duration)-1)*100 for i in return_series_list]
    annual_sample = len(diff_return)/duration # 计算一年有多少条记录
    # 年化sharpe
    diff_sharpe = diff_return.mean()/diff_return.std()*np.sqrt(annual_sample)
    sharpe_list = [return_series[i].mean()/return_series[i].std()*np.sqrt(annual_sample) for i in return_series]
    # 计算单调性分数
    monotonous_score = monotonous(return_series)
    if showfig:
        # 可视化输出
        data = [go.Scatter(y=num*100-100,x=return_series.index,mode='lines',
                           name='Best {}%'.format((i+1)/len(return_series_list)*100),
                           line = dict(color=color_list[i],width=2))
                for i,num in enumerate(return_series_list)]
        data += [go.Scatter(y=(diff_return_list-1)*100,x=diff_return.index,mode='lines',
                            line = dict(color=color_list[-1],width=4),name='多空对冲')]
        pos_diff = diff_return[diff_return>0]*100
        neg_diff = diff_return[diff_return<=0]*100
        success_prob = len(pos_diff)/len(diff_return)
        pos_bar = go.Bar(
          x = pos_diff.index,
          y = pos_diff.values,
          marker = dict(color='rgba(215,84,66,0.8)'),
          name = 'positive return'
        )
        neg_bar = go.Bar(
          x = neg_diff.index,
          y = neg_diff.values,
          marker = dict(color='rgba(107,165,131,0.8)'),
          name = 'negative return'
        )
        from plotly import tools
        fig = tools.make_subplots(rows=2,cols=1,shared_xaxes=True)
        fig.append_trace(pos_bar,2,1)
        fig.append_trace(neg_bar,2,1)
        for line in data:
            fig.append_trace(line,1,1)
        fig.layout.yaxis1.domain=[0.2,1.0]
        fig.layout.yaxis2.domain=[0.0,0.22]
        fig.layout.yaxis1.ticksuffix='%'
        fig.layout.yaxis2.ticksuffix='%'
        fig.layout.title='多空对冲年化收益率{:.1f}%<br>夏普:{:.4f} 胜率:{:.3f} 单调:{:.3f}'\
                         .format(annual_diff_return,diff_sharpe,success_prob,monotonous_score)
        if notebook_mode:
            init_notebook_mode()
            iplot(fig, validate=False, show_link=False)
        else:
            plot(fig, filename='report.html', validate=False, show_link=False)

    result = {'return':np.array([i[-1] for i in return_series_list]),
              'sharpe':np.array(sharpe_list),
              'diff_return':diff_return_list[-1]-1,
              'diff_sharpe':diff_sharpe,
              'monotonous':monotonous_score}
    return result

def feature_valid_test(feature, instrument_ids, time_range, notebook_mode=True, showfig=True):
    '''
    Fast test for 'feature' obj
    Use ops to Decorate feature and test its validation
    '''
    feature_name = str(feature)
    features = [feature, ChangeRate_Daily(), 
                Shift(ChangeRate_Daily(),-1)]
    dataset = load_dataset(instrument_ids, time_range, features)
    dataset.columns.values[-1]='pct_change'
    dataset.columns.values[-2]='limit'
    return valid_test(dataset, feature_name, notebook_mode=notebook_mode, showfig=showfig)

if __name__ == '__main__':
    test = np.random.random([5,1000])
    print(monotonous(test))
