import plotly.plotly as py
import plotly.graph_objs as go
pwval = [.9506, 0.98, 0.796, 0.87023 , .90, 1.0, 0.7142, .941  ]
clrgrey = 'rgb(204,204,204)'
clrred = 'rgb(222,45,38)'
clrs  = [clrred if pwval[x] != 0 else clrgrey for x in range(len(pwval))]
data = [go.Bar(
            x=pwval,
            y=['Galaxy S8+', 'Galaxy Note8', 'iPhone 8 Plus', 'Galaxy S8', 'Galaxy S9', 'iPhone X', 'iPhone 8', 'Galaxy S9+'],
            orientation = 'h',
            name='Performance',
            marker=dict(color=clrs)
            
)]
#data = [trace0]
layout = go.Layout(
    title='Performance',
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='horizontal-bar')