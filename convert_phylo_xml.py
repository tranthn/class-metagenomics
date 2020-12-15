#!/usr/bin/env python3
import sys
import json
import xmltodict
import argparse

# utility method that takes in an XML file and converts
# the file into a Python dictionary that we can modify
def xml_to_json(file_name):
    try:
        with open(file_name) as f:
            output = xmltodict.parse(f.read())
        return output
    except:
        print('\nThere was an issue reading XML input file, exiting...\n')
        sys.exit(1)

# writes out the phyloXML to JSON representation to a file
def write_out_json(phylo_json, fname):
    try:
        with open(fname, 'w') as f:
            print('\nWriting out json to: {0}\n'.format(fname))
            f.write(phylo_json)
    except:
        print('\nThere was an issue writing out the JSON file, exiting...\n')
        sys.exit(1)

# tidies up the taxon name for a clade
# phyloSift outputs its clade names as so: _SOMENAME_{taxon ID}
# we will convert it to a slightly more readable form: SOMENAME (taxon ID)
def tidyup_clade_names(name):
    tidy = name.replace('__', ' ').replace('_', ' ').strip()
    tidy = tidy.replace('{', '(').replace('}', ')')
    return tidy

# writes out the data arrays to a file
# file will contain 1 array per line, as plain string, e.g:
#   ['parent', 'child1']
#   ['child1', 'child2']
#   [1, 1]
#
# this will be used / loaded by the `plotly-phylo.py` script
def write_out_plotly(parents, children, values, fname):
    try:
        with open(fname, 'w') as f:
            f.write(str(parents))
            f.write('\n')
            f.write(str(children))
            f.write('\n')
            f.write(str(values))
            print('\nWriting out Plotly arrays to: {0}\n'.format(fname))
    except:
        print('\nThere was an issue writing out the Plotly file, exiting...\n')
        sys.exit(1)

# utility function used during debugging, to determine maximal tree depth of phyloXML -> dictionary
def find_max_depth(root):
    if 'clade' in root.keys():
        return 1 + max([0] + list(map(find_max_depth, root['clade'])))
    else:
        return 1

# modifies Python dictionary structure in-place
# as it walks down the tree, it will count the depth
# once it reaches the maximum specified depth on a given note
# it will prune the remaining subtree
#
# this allow users to generate more simplified / smaller JSON files if desired
def traverse_depth(root, max_depth = None, depth = None):
    if root['name']:
        root['name'] = tidyup_clade_names(root['name'])

    if 'clade' in root.keys():
        if (not max_depth is None) and (depth == max_depth):
            root['value'] = 1
            root.pop('clade')
        else:
            depth += 1
            [traverse_depth(x, max_depth, depth) for x in root['clade']]
    else:
        root['value'] = 1

# walks the tree to create 2 flat arrays represent parent nodes and child nodes
# example:
#   parents = ['parent1', 'parent2']
#   children = ['child1', 'child2']
#
def flatten_plotly(root, parents = [], children = [], parent = 'root'):
    if 'clade' in root.keys():
        parents.append(parent)
        children.append(root['name'])
        [flatten_plotly(x, parents, children, root['name']) for x in root['clade']]
    else:
        parents.append(parent)
        children.append(root['name'])

######################################## main #######################################
#####################################################################################
parser = argparse.ArgumentParser(description='Converts a phyloXML file to nested JSON (D3.js) or flat arrays (Plotly)')
parser.add_argument('-i', '--input', dest='input', help='phyloXML file path, must be XML', required=True)
parser.add_argument('-o', '--output', dest='output', help='output file name, e.g. test.json or plotly.out', required=False)
parser.add_argument('-p', '--plot-type', dest='plottype', help='which plot library format to conver to, options = [plotly, d3]', required=True)
parser.add_argument('-d', '--max-depth', dest='maxdepth', help='max depth of the output JSON file, default = 5, -1 = no maximum', default = 5)
args = parser.parse_args()

# reads in arguments, only max_depth is not required so we will do a check
#####################################################################################
input_file = args.input
output_file = args.output
max_depth = int(args.maxdepth)
plot_type = args.plottype

if max_depth == -1:
    max_depth = None

# early exit if our input file is invalid
if not input_file.endswith('.xml'):
    print('\nInvalid input file format, expecting XML, exiting...\n')
    sys.exit(1)

# if there was no output_file set, we'll contextually set it
if output_file is None:
    parts = input_file.split('.xml')
    output_file_prefix = parts[0]
    output_file_suffix = '.json' if plot_type == 'd3' else '.out'
    output_file = output_file_prefix + output_file_suffix

#####################################################################################

# for either D3 or Plotly output, we will still need to read XML to Python dictionary
# we will also traverse down the tree to get the first parent clade
# the root clade will simply be called "root"
out = xml_to_json(input_file)
subtree = out['phyloxml']['phylogeny']['clade']
subtree['name'] = 'root'

# modifies the subtree in place to prune any subtrees that go beyond maximum tree depth
traverse_depth(subtree, max_depth = max_depth, depth = 0)

if (plot_type == 'd3'):
    # produce json for python d3 graph
    json = json.dumps(subtree)
    json = json.replace("clade", "children")
    write_out_json(json, output_file)
elif (plot_type == 'plotly'):
    # produce flattened arrays for plotly graph
    # reuses json structure from d3
    parents = []
    children = []
    flatten_plotly(subtree, parents, children, '')
    k = len(parents)
    values = [1] * k
    write_out_plotly(parents, children, values, output_file)