#!/usr/bin/env python3
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
from ete3 import ClusterTree, TreeStyle
from itertools import combinations

def read_values_from_file(fname):
    with open(fname) as f:
        parents = eval(f.readline())
        children = eval(f.readline())
        values = eval(f.readline())

    data_dic = dict(
        parents = parents,
        children = children,
        values = values
    )
    return data_dic

data = read_values_from_file('../plotly.out')

fig = px.sunburst(
    data,
    parents="parents",
    names="children",
    values="values",
)
fig.show()

######################################################################

# newickstr = "(Bovine:0.69395,(Gibbon:0.36079,(Orang:0.33636,(Gorilla:0.17147,(Chimp:0.19268, Human:0.11927):0.08386):0.06124):0.15057):0.54939,Mouse:1.21460):0.10;"
# # tree = ClusterTree('(A:0.1,B:0.2,(C:0.3,D:0.4):0.5);')
# tree = ClusterTree(newickstr)
# leaves = tree.get_leaf_names()
# # idx_dict = {'A':0,'B':1,'C':2,'D':3}
# idx_dict = {'Bovine': 0, 'Gibbon': 1, 'Orang': 2, 'Gorilla': 3, 'Chimp': 4, 'Human': 5, 'Mouse': 6}
# dict_keys = list(idx_dict.keys())
# dict_values = list(idx_dict.values())
# idx_labels = [dict_keys[dict_values.index(i)] for i in range(0, len(idx_dict))]

# dmat = np.zeros((7,7))

# for l1,l2 in combinations(leaves,2):
#     d = tree.get_distance(l1,l2)
#     dmat[idx_dict[l1],idx_dict[l2]] = dmat[idx_dict[l2],idx_dict[l1]] = d

# labels = dict_keys
# fig = ff.create_dendrogram(dmat, labels = labels, orientation = 'left')
# fig.update_layout(width=1200, height=800)
# fig.show()

