#!/usr/bin/env python3
# import ete3
from ete3 import ClusterTree
import scipy.cluster.hierarchy as sch
import scipy.spatial.distance
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations

tree = ClusterTree('(A:0.1,B:0.2,(C:0.3,D:0.4):0.5);')
leaves = tree.get_leaf_names()
idx_dict = {'A':0,'B':1,'C':2,'D':3}
dict_keys = list(idx_dict.keys())
dict_values = list(idx_dict.values())
idx_labels = [dict_keys[dict_values.index(i)] for i in range(0, len(idx_dict))]

#just going through the construction in my head, this is what we should get in the end
my_link = [[0,1,0.3,2],
        [2,3,0.7,2],
        [4,5,1.0,4]]

my_link = np.array(my_link)
dmat = np.zeros((4,4))

for l1,l2 in combinations(leaves,2):
    d = tree.get_distance(l1,l2)
    dmat[idx_dict[l1],idx_dict[l2]] = dmat[idx_dict[l2],idx_dict[l1]] = d

print('Distance matrix')
print(dmat)
print()

schlink = sch.linkage(scipy.spatial.distance.squareform(dmat),method='average',metric='euclidean')

print('Linkage from scipy')
print(schlink)
print()

print('My link')
print(my_link)
print()

print('Was linkage matrix correct?\n', schlink == my_link)

dendro = sch.dendrogram(my_link,labels=idx_labels)
plt.show()