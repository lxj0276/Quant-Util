# -*- coding: utf-8 -*-
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.offline import init_notebook_mode, iplot, plot


def plot_charts(days, day_returns, index_returns, table, notebook_mode=True):

    fig = ff.create_table(table, height_constant=10)
    
    strategy = go.Scatter(
        name=u'策略收益',
        x=days,
        y=day_returns,
        xaxis='x2',
        yaxis='y2',
    )

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
    
    fig['data'].extend(go.Data([strategy, benchmark]))
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

    return fig
