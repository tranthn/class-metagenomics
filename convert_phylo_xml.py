#!/usr/bin/env python3
import json
import xmltodict

def xml_to_json(file_name):
    with open(file_name) as f:
        output = xmltodict.parse(f.read())
    return output

def write_out_json(phylo, fname):
    with open(fname, 'w') as f:
        f.write(phylo)

def max_depth(root):
    if 'clade' in root.keys():
        return 1 + max([0] + list(map(max_depth, root['clade'])))
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
        print('parent-child {0} <- {1}'.format(parent, root['name']))
        parents.append(parent)
        children.append(root['name'])
        [flatten_plotly(x, parents, children, root['name']) for x in root['clade']]
    else:
        parents.append(parent)
        children.append(root['name'])

###########################################################################
input_file = '../data/phyloxml-hmp.xml'
output_file = 'phylo-test.json'
# output_file = 'test.json'
# input_file = '../data/test.xml'

out = xml_to_json(input_file)
unnest = out['phyloxml']['phylogeny']['clade']
unnest['name'] = 'root'

# produce json for python d3 graph
traverse_depth(unnest, max_depth = 4, depth = 0)
# json = json.dumps(unnest)
# json = json.replace("clade", "children")
# write_out_json(json, output_file)

# produce flattened arrays for plotly graph
# reuses json structure from d3
parents = []
children = []
flatten_plotly(unnest, parents, children, '')
print()
print(parents)
print()
print(children)
print()
k = len(parents)
values = [1] * k
print(values)