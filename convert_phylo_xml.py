#!/usr/bin/env python3
import json
import xmltodict
# import re
# import xml.etree.cElementTree as etree
# from Bio import Phylo


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
        if (depth == max_depth):
            root['value'] = 1
            root.pop('clade')
        else:
            depth += 1
            [traverse_depth(x, max_depth, depth) for x in root['clade']]

    else:
        root['value'] = 1

###########################################################################
input_file = '../data/phyloxml-hmp.xml'
output_file = 'phylo-test.json'
# output_file = 'test.json'
# input_file = '../data/test.xml'

out = xml_to_json(input_file)
unnest = out['phyloxml']['phylogeny']['clade']
unnest['name'] = 'root'

traverse_depth(unnest, max_depth = 6, depth = 0)
# depth = max_depth(unnest)
# print('max depth', depth)

json = json.dumps(unnest)
json = json.replace("clade", "children")
write_out_json(json, output_file)