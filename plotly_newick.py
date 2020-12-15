#!/usr/bin/env python3
import argparse
import plotly.figure_factory as ff
import numpy as np
from ete3 import Tree
from itertools import combinations

# since newick is more simplified with only branch lengths
# we will need to back-calculate the distance matrix
# to be able to feed in the right data structure to the Plotly denodrgram
def calculate_distance_matrix(fname):
    tree = Tree(fname, quoted_node_names=True, format=1)
    leaves = tree.get_leaf_names()
    k = len(leaves)

    # converts the leaf nodes in dictionary mapping the name: index
    idx_dict  = {}
    for idx, leaf in enumerate(leaves):
        idx_dict[leaf] = idx

    # this backtracks to generate the distance matrix given the branch lengths
    # and nested structure from the newick format, since the latter condenses information
    dict_keys = list(idx_dict.keys())
    dict_values = list(idx_dict.values())
    idx_labels = [dict_keys[dict_values.index(i)] for i in range(0, len(idx_dict))]
    dist_matrix = np.zeros((k, k))

    # goes through all the possible 2-leaf (pair) combos
    # uses the ClusterTree utility to get the distance between the leaves
    # stores the distance symmetrically, i.e. distance from leaf1 -> leaf2 is the same as leaf2 -> leaf1 
    for leaf1, leaf2 in combinations(leaves, 2):
        d = tree.get_distance(leaf1,leaf2)
        dist_matrix[idx_dict[leaf1], idx_dict[leaf2]] = dist_matrix[idx_dict[leaf2], idx_dict[leaf1]] = d

    return dist_matrix, leaves

# main method to calculate distance matrix
# draws the dendrogram figure and outputs it to an HTML file
def draw_dendrogram(input_file, output_file):
    dist_matrix, labels = calculate_distance_matrix(input_file)

    # generate dendrogram given the calculated distance matrix
    fig = ff.create_dendrogram(dist_matrix, labels = labels, orientation = 'left')
    fig.update_layout(width = 1200, height = 1200)
    print('\nSaving dendrogram diagram to: {0}\n'.format(output_file))
    fig.write_html(output_file)

################# main #################
parser = argparse.ArgumentParser(description='Generate a Plotly sunburst graph as HTML')
parser.add_argument('-i', '--input', dest='input', help='plotly input file path, output from the convert_phylo_xml script', required=True)
parser.add_argument('-o', '--output', dest='output', help='plotly output HTML file path', required=False)
args = parser.parse_args()

input_file = args.input
output_file = args.output

# if there was no output_file set, we'll contextually set it
if output_file is None:
    output_file = input_file + '.html'

draw_dendrogram(input_file, output_file)