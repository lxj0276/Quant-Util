# -*- coding: utf-8 -*-
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.offline import init_notebook_mode, iplot, plot
from .utils import risk_analysis


def plot_chart(dates, returns, notebook_mode=False):

    dates = pd.to_datetime(dates)
    total_return, annual_return, sharpe_ratio, (begin, end, drawdown) = risk_analysis(returns)
    table = [
        ('累计收益', str(round(total_return[-1]*100, 2))+'%'),
        ('年化收益', str(round(annual_return*100, 2))+'%'),
        ('夏普比率', str(round(sharpe_ratio,3))),
        ('最大回撤', str(round(drawdown*100, 3))+'%'),
        ('最大回撤天数', str(end-begin)),
    ]
    table = list(map(list, zip(*table)))
    fig = ff.create_table(table, height_constant=10)
    strategy = go.Scatter(
        name='策略收益',
        x=dates,
        y=total_return*100,
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

    fig['data'].extend(go.Data([strategy]))
    fig.layout.update(layout)
    fig.layout.yaxis2.update({'anchor': 'x2'})
    fig.layout.xaxis2.update({'anchor': 'y2'})
    fig.layout.margin.update({'t':50, 'b':50, 'l':50, 'r':80})
    fig.layout.update({'height': 400})

    if notebook_mode:
        init_notebook_mode()
        iplot(fig, validate=False, show_link=False)
    else:
        plot(fig, filename='report.html', validate=False, show_link=False)
