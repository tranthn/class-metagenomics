#!/usr/bin/env python3
import sys
import json
import xml.etree.cElementTree as etree
from Bio import Phylo
import xmltodict

def xml_to_json(file_name):
    with open(file_name) as f:
        output = xmltodict.parse(f.read())
    return output

def write_out_json(phylo, fname):
    with open(fname, 'w') as f:
        f.write(phylo)

def rename_dict_key(d, old_key, new_key):
    for k,v in d.items():
        if k == old_key:
            d[new_key] = d.pop(old_key)
        if isinstance(v, dict):
            rename_dict_key(v, old_key, new_key)

###########################################################################
# fname = '../data/phyloxml-hmp.xml'
fname = '../data/test.xml'
out = xml_to_json(fname)
rename_dict_key(out, 'clade', 'children')
print(out)
unnest = out['phyloxml']['phylogeny']['children']
unnest['name'] = 'root'
json = json.dumps(unnest)
write_out_json(json, 'test_out.json')