import math
import os
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot, plot

from engine.cons import INDEX_DATA_PATH
from engine.env import RISK_FREE_RATE
from engine.utils import max_drop_down


def create_table(market_values, benchmark=None):
    """market_values should be series with date index """
    daily_1p_return = market_values / market_values.shift(1)
    total_return = market_values / market_values.iloc[0]
    maxdropdown, mdd = max_drop_down(total_return)
    annualreturn = math.pow(total_return.iloc[-1], 250 / len(total_return)) - 1

    dayreturnstd = np.std(daily_1p_return, ddof=1)
    if dayreturnstd == 0:
        sharp = 0
    else:
        sharp = (annualreturn - RISK_FREE_RATE) / (dayreturnstd * np.sqrt(250))

    table = [
        (u'回测收益', str(round((total_return.iloc[-1] - 1) * 100, 2)) + '%'),
        (u'年化收益', str(round(annualreturn * 100, 2)) + '%'),
        (u'夏普比率', str(round(sharp, 3))),
        (u'最大回撤', str(round(maxdropdown * 100, 3)) + '%'),
        (u'最大回撤天数', str(mdd)),
    ]
    if benchmark != None:
        index_close = \
        pd.read_csv(os.path.join(INDEX_DATA_PATH, benchmark + '.csv'))[['date', 'close']].set_index('date')['close']
        index_close = index_close.reindex(total_return.index)
        index_returns = index_close / index_close.iloc[0]
        index_returns = index_returns.values
        # index_returns.index = map(lambda x: datetime.strptime(str(x), '%Y%m%d'), index_returns.index)


    else:
        index_returns = None

    total_return.index = map(lambda x: datetime.strptime(str(x), '%Y%m%d'), total_return.index)

    return total_return, index_returns, table


def plot_charts(days, day_returns, table, index_returns=None, notebook_mode=True):
    fig = ff.create_table(table, height_constant=10)

    strategy = go.Scatter(
        name=u'策略收益',
        x=days,
        y=day_returns,
        xaxis='x2',
        yaxis='y2',
    )
    if not (index_returns is None):
        benchmark = go.Scatter(
            name=u'基准收益',
            x=days,
            y=index_returns,
            xaxis='x2',
            yaxis='y2',
        )

    layout = dict(
        xaxis={
            'rangeslider': {
                'visible': False,
            }
        },
        yaxis={
            'domain': [0.8, 1]
        },
        xaxis2={
            'side': 'bottom',
            'rangeslider': {
                'visible': False,
            }
        },
        yaxis2={
            'domain': [0, 0.75],
            'side': 'right',
            'ticksuffix': '%',
        },
        legend={
            'x': 0,
            'y': 0.8,
            'orientation': 'h'
        }
    )
    if index_returns is None:
        fig['data'].extend(go.Data([strategy]))
    else:
        fig['data'].extend(go.Data([strategy, benchmark]))
    fig.layout.update(layout)
    fig.layout.yaxis2.update({'anchor': 'x2'})
    fig.layout.xaxis2.update({'anchor': 'y2'})
    fig.layout.margin.update({'t': 50, 'b': 50, 'l': 50, 'r': 80})
    fig.layout.update({'height': 400})

    if notebook_mode:
        init_notebook_mode()
        iplot(fig, validate=False, show_link=False)
    else:
        plot(fig, filename='report.html', validate=False, show_link=False)

    return fig


def plot_charts_with_market_value(market_values, notebook_mode=True, benchmark=None):
    total_return, index_returns, table = create_table(market_values, benchmark=benchmark)
    total_return = total_return * 100 - 100
    if not index_returns is None:
        index_returns = index_returns * 100 - 100
    return plot_charts(list(total_return.index), list(total_return), table, notebook_mode=notebook_mode,
                       index_returns=list(index_returns))
