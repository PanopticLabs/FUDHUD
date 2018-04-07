import plotly.offline as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import pandas as pd

def plotGraph(csvfile, xlabel, y1label, y2label, title, y1title, y2title):
    data = pd.read_csv(csvfile, delimiter=',')
    data[xlabel] = pd.to_datetime(data[xlabel])

    trace0 = go.Scatter(
        x = data[xlabel],
        y = data[y1label],
        mode = 'lines+markers',
        name = y1title,
        line=dict(
            shape='spline'
        )
    )
    trace1 = go.Scatter(
        x = data[xlabel],
        y = data[y2label],
        mode = 'lines+markers',
        name = y2title,
        yaxis = 'y2',
        line=dict(
            shape='spline'
        )
    )

    plot = [trace0, trace1]

    layout = go.Layout(
        title=title,
        yaxis=dict(
            title=y1title
        ),
        yaxis2=dict(
            title=y2title,
            titlefont=dict(
                color='rgb(148, 103, 189)'
            ),
            tickfont=dict(
                color='rgb(148, 103, 189)'
            ),
            overlaying='y',
            side='right'
        )
    )
    fn = title.lower().replace(' ', '-')
    fig = go.Figure(data=plot, layout=layout)
    py.plot(fig, filename='viz/' + fn + '.html')

#plotGraph('csv/btc.csv', 'Date', 'Bitcoin Trends', 'Historical Price (USD)', 'Bitcoin Trends vs Price', 'Bitcoin Trends', 'Historical Price (USD)')
