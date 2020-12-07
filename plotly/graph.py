#!/usr/bin/env python3
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np

data = dict(
    character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
    parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
    value=[10, 14, 12, 10, 2, 6, 6, 4, 4])

fig = px.sunburst(
    data,
    names='character',
    parents='parent',
    values='value',
)
fig.show()

######################################################################
X = np.array([
    [1, 0.1],
    [1, 0.2],
    [0.5, 0.3],
    [0.7, 0.4]
])
labels = ['A', 'B', 'C', 'D']
# fig = ff.create_dendrogram(X, labels = labels)
# fig.update_layout(width=900, height=500)
# fig.show()