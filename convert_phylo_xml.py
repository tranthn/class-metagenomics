#!/usr/bin/env python3
import sys
import json
import xml.etree.cElementTree as etree
from Bio import Phylo
import xmltodict

def parseXML(file_name):
    # Parse XML with ElementTree
    tree = etree.ElementTree(file=file_name)
    root = tree.getroot()

    # get the information via the children!
    print("-" * 25)
    print("Iterating using getchildren()")
    print("-" * 25)
    print()
    print(root)
    for node in root:
        for child in node:
            print("{0} = {1}".format(child.tag, child.text))

        print()

def parseBio(file_name):
    tree = Phylo.read(file_name,'phyloxml')
    return tree
    # print(tree)

def xml_to_json(file_name):
    with open(file_name) as f:
        output = xmltodict.parse(f.read())
    
    return output

def write_out_json(xml_dict, fname):
    with open(fname, 'w') as f:
        f.write(xml_dict)

###########################################################################
# parseXML('../data/books.xml')
# parseXML('../data/test.xml')
# parseBio('../data/test.xml')
# tree = parseBio('../data/phyloxml-hmp.xml')
# Phylo.draw_ascii(tree)

# out = xml_to_json('../data/books.xml')
# out = xml_to_json('../data/test.xml')
fname = '../data/phyloxml-hmp.xml'
fname = '../data/test.xml'
out = xml_to_json(fname)
json = json.dumps(out)
write_out_json(json, 'test_out.json')
