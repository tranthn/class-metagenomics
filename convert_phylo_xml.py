#!/usr/bin/env python3
import json
import xmltodict
import argparse

def xml_to_json(file_name):
    with open(file_name) as f:
        output = xmltodict.parse(f.read())
    return output

def write_out_json(phylo, fname):
    with open(fname, 'w') as f:
        f.write(phylo)

def write_out_plotly(parents, children, values, fname):
    with open(fname, 'w') as f:
        f.write(str(parents))
        f.write('\n')
        f.write(str(children))
        f.write('\n')
        f.write(str(values))

def find_max_depth(root):
    if 'clade' in root.keys():
        return 1 + max([0] + list(map(find_max_depth, root['clade'])))
    else:
        return 1

def traverse_depth(root, max_depth = None, depth = 0):
    if 'clade' in root.keys():
        if (not max_depth is None) and (depth == max_depth):
            root['value'] = 1
            root.pop('clade')
        else:
            depth += 1
            [traverse_depth(x, max_depth, depth) for x in root['clade']]
    else:
        root['value'] = 1

def flatten_plotly(root, parents = [], children = [], parent = 'root'):
    if 'clade' in root.keys():
        parents.append(parent)
        children.append(root['name'])
        [flatten_plotly(x, parents, children, root['name']) for x in root['clade']]
    else:
        parents.append(parent)
        children.append(root['name'])

################# main #################
parser = argparse.ArgumentParser(description='Converts a phyloXML file to nested JSON')
parser.add_argument('-i', '--input', dest='input', help='phyloXML file path', required=True)
parser.add_argument('-o', '--output', dest='output', help='output file name', required=True)
parser.add_argument('-p', '--plot-type', dest='plottype', help='which plot library format to conver to, options = [plotly, d3]', required=True)
parser.add_argument('-d', '--max-depth', dest='maxdepth', help='max depth of the output JSON file, default = 5, -1 = no maximum', default = 5)
args = parser.parse_args()

input_file = args.input
output_file = args.output
max_depth = int(args.maxdepth)
plot_type = args.plottype

if max_depth == -1:
    max_depth = None

out = xml_to_json(input_file)
unnest = out['phyloxml']['phylogeny']['clade']
unnest['name'] = 'root'

traverse_depth(unnest, max_depth = max_depth, depth = 0)

if (plot_type == 'd3'):
    # produce json for python d3 graph
    json = json.dumps(unnest)
    json = json.replace("clade", "children")
    write_out_json(json, output_file)
elif (plot_type == 'plotly'):
    # produce flattened arrays for plotly graph
    # reuses json structure from d3
    parents = []
    children = []
    flatten_plotly(unnest, parents, children, '')
    k = len(parents)
    values = [1] * k
    write_out_plotly(parents, children, values, output_file)