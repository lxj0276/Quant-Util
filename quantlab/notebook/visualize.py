# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division

import numpy as np
import pandas as pd
import itertools


def plotly_colors(n):
    return ['hsl(' + str(h) + ',50%'+',50%)' for h in np.linspace(0, 360, n + 1)[:-1]]


def plot_box(data, title=None, boxpoints=False, boxmean=False, showlegend=False, colors=None, as_figure=False):
    """ box plot with mean and stdev.

    Parameters
    ----------
    data : Iterable of (name, values) tuples. Names are used in x axis, values are used to plot the box plot.

    Returns
    ----------
    fig : if as_figure == True
    data : if as_figure == 'data'
    None : plot directly and return None if as_figure == False
    """
    import plotly
    import plotly.graph_objs as go
    plotly.offline.init_notebook_mode()

    if type(colors) != list:
        colors = [colors] * len(data)

    data = [
        {
            'name': n,
            'y': d,
            'type': 'box',
            'boxpoints': boxpoints,
            'boxmean': boxmean,
            'marker':{'color': colors[i]}
        }
        for i, (n, d) in enumerate(data)
        ]

    layout = {
        'showlegend': showlegend,
        'title': title,
    }

    fig = go.Figure(data=data, layout=layout)

    if as_figure == True:
        return fig
    elif as_figure == 'data':
        return data
    elif as_figure == False:
        plotly.offline.iplot(fig)
        return None
    else:
        raise RuntimeError('Unsupported value for `as_figure`: %s' % as_figure)

def plot_score_metrics(scores, labels, pct_change,  kind='scatter', data_points=1000):
    """ plot score metrics.

    Parameters
    ----------
    scores : prediction probability as 1-d array
    labels : binary labels as 1-d array
    pct_change : percent change of real price

    Returns
    ----------
    """
    import cufflinks as cf
    cf.set_config_file(offline=True, world_readable=False, theme='white', offline_show_link=False)

    scores = np.array(scores)
    labels = np.array(labels)
    pct_change = np.array(pct_change)

    l = scores.shape[0]
    log_return = np.log1p(pct_change)
    abs_log_return = np.abs(log_return)
    base = pd.DataFrame({
        'Score': scores,
        'Label': labels,
        'Log Return': log_return,
        'Abs. Log Return': abs_log_return,
    })

    df = base.sort_values('Score').reset_index(drop=True)
    df['Cum. Log Return'] = df['Log Return'][::-1].cumsum()[::-1]
    df['Index'] = range(l)
    df.set_index('Index', inplace=True)
    dft = base.sort_values('Log Return').reset_index(drop=True)
    dft['Cum. Log Return'] = dft['Log Return'][::-1].cumsum()[::-1]
    dft['Index'] = range(l)
    dft.set_index('Index', inplace=True)

    best_cum_log_return = df['Cum. Log Return'].max()
    print('Best cum. log return = %s' % best_cum_log_return)
    base_triangle_area = (dft.ix[0, 'Cum. Log Return'] + dft.ix[l - 1, 'Cum. Log Return']) * l / 2
    oracle_gainloss_auc = dft['Cum. Log Return'].sum() - base_triangle_area
    gainloss_auc = df['Cum. Log Return'].sum() - base_triangle_area
    print('Gain/loss AUC = %s' % (gainloss_auc / oracle_gainloss_auc))

    # Plotting
    if kind == 'scatter':
        if data_points is None:
            data_points = 3000
        stride, extra = divmod(l, data_points)
        if stride < 1:
            stride, extra = (1, 0)

        plot_df = df.iloc[::stride]
        plot_dft = dft.iloc[::stride]
        if extra != 1:
            plot_df = pd.concat([plot_df, df.iloc[l - 1:l]])
            plot_dft = pd.concat([plot_dft, dft.iloc[l - 1:l]])

        plot_df.iplot(title='Test', subplots=True)
        plot_df.iplot(title='Test')

        plot_dft.iplot(title='Oracle', subplots=True)
        plot_dft.iplot(title='Oracle')

    elif kind == 'box':
        if data_points is None:
            data_points = 20
        stride, extra = divmod(l, data_points)
        if stride < 1:
            stride, extra = (1, 0)
        if extra:
            stride += 1

        def plot_boxes_for_df(df, title):
            columns = df.columns
            cc = len(columns)
            cs = plotly_colors(cc)

            df = df.values
            for ci in range(cc):
                data = []
                for _, g in itertools.groupby(enumerate(df[:, ci]), lambda x: x[0] // stride):
                    g = np.asarray(list(g))
                    data.append(('%d ~ %d' % (g[0, 0], g[-1, 0]), g[:, 1]))
                plot_box(data, boxmean='sd', colors=cs[ci], title=title + ' - ' + columns[ci])

        plot_boxes_for_df(df, 'Test')
        plot_boxes_for_df(dft, 'Oracle')
    else:
        raise RuntimeError('Unsupported value for `kind`: %s' % kind)


def plot_dsat(pct_change, score, metadata, marketdata, N=5, lookback=60, lookfuture=30, color_inverse=True):
    """ plot dissatisfaction cases in prediction.
    both FP & FN will be considered.
    NOTE: please keep your index sorted along time.
    
    Parameters
    ----------
    pct_change    : original percent change of price
    score         : model prediction score
    metadata      : sample metadata as dataframe
    marketdata    : original market data for plotting
    N             : number of worst cases to visualize
    lookback      : days count to look back
    lookfuture    : days count to look future
    color_inverse : whether inverse increase & decrease color
    
    Returns
    ----------
    N worst cases as dataframe
    
    Examples
    ----------
    """
    import numpy as np
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.figure_factory as ff
    from plotly import tools
    from plotly.offline import init_notebook_mode, iplot
    from IPython.display import display, HTML
    
    init_notebook_mode()
    
    # validate
    try:
        assert len(score) == len(pct_change) == len(metadata)
    except:
        print('ERROR: pct_change/score/metadata should have same length')
        return
    try:
        assert 'date' in metadata and 'code' in metadata
    except:
        print('ERROR: date/code should in metadata columns')
        return
    try:
        assert len(set([x for x in marketdata.columns if x in ['date', 'code', 'open', 'high', 'low', 'close', 'volume']])) == 7
    except:
        print('ERROR: date/code/open/high/low/close/volume should in marketdata columns')
        return
    
    # numpify
    score = np.array(score)
    pct_change = np.array(pct_change)
    
    # select N worst cases
    loss = score*pct_change
    worst_index = np.argsort(loss)[:N]

    ret = []
    for i, idx in enumerate(worst_index):
        
        meta = metadata.iloc[idx:idx+1].round(6)
        ret.append(meta)
        
        market = marketdata[marketdata.code==meta.code.iloc[0]].reset_index(drop=True)
        midx = market[market.date==meta.date.iloc[0]].index[0]
        lower = max(midx-lookback, 0)
        upper = midx+lookback
        date = market.iloc[lower:upper].date
        open = market.iloc[lower:upper].open
        high = market.iloc[lower:upper].high
        low  = market.iloc[lower:upper].low
        close= market.iloc[lower:upper].close
        volume = market.iloc[lower:upper].volume
        
        fig = ff.create_table(meta, height_constant=10)
        
        trace_volume = go.Bar(
            name='Volume',
            x=date,
            y=volume,
            xaxis='x2',
            yaxis='y2',
            marker={
                'color': 'rgba(55, 128, 191, 1.0)',
            },
            showlegend=False,
        )
        
        trace_price = go.Candlestick(
            x=date,
            open=open,
            high=high,
            low=low,
            close=close,
            xaxis='x2',
            yaxis='y3',
            increasing={
                'name':  '',
                'showlegend': False,
                'line':{
                    'color': 'rgb(255, 65, 54)' if color_inverse else 'rgb(61, 153, 112)',
                }
            },
            decreasing={
                'name':  '',
                'showlegend': False,
                'line':{
                    'color': 'rgb(61, 153, 112)' if color_inverse else 'rgb(255, 65, 54)',
                }
            }
        )

        trace_marker = go.Scatter(
            name='',
            x=[market.iloc[midx].date],
            y=[market.iloc[midx].low],
            xaxis='x2',
            yaxis='y3',
            hoverinfo='skip',
            showlegend=False,
            marker={
                'symbol': 'triangle-up-open',
                'color': 'black',
                'size': 10
            }
        )
        
        layout = dict(
            xaxis={
                'rangeslider': {
                    'visible': False,
                }
            },
            yaxis={
                'domain': [0.9, 1]
            },
            xaxis2={
                'side': 'bottom',
                'rangeslider': {
                    'visible': False,
                }
            },
            yaxis2={
                'domain': [0, 0.15],
            },
            yaxis3={
                'domain': [0.15, 0.85],
            }
        )
        fig['data'].extend(go.Data([trace_price, trace_volume, trace_marker]))
        fig.layout.update(layout)
        fig.layout.yaxis2.update({'anchor': 'x2'})
        fig.layout.xaxis2.update({'anchor': 'y2'})
        fig.layout.yaxis3.update({'anchor': 'x2'})
        fig.layout.margin.update({'t':50, 'b':50, 'l':50, 'r':50})
        fig.layout.update({'height': 600})
        fig.layout.update({'title': 'No.%d' % (i+1)})
        iplot(fig, validate=False, show_link=False)

    ret = pd.concat(ret)
    return ret
