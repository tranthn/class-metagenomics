#!/usr/bin/env python3
import sys
import json
import os
import argparse
from sam import SAM
import graph

global name_maps
global out

# parses filtered SAM file that only contains aligned reads
#
# arguments:
#   - input: file path to SAM file
#
# returns
#   - list of parsed SAM reads objects, using imported SAM class
def process_sam_file(input):
    sam_reads = []
    identities = []
    coords = []

    if input != "":
        try:
            with open(input, 'r') as inp:
                for l in inp:

                    # skip header lines, except for SN/LN
                    if (l.startswith('@')):
                        if 'LN:' in l or 'SN:' in l:
                            # splits header into 3 parts: @SQ, SN, LN
                            parts = l.split('\t')
                            ref_name = parts[1].split('SN:')[1]
                            length = int(parts[2].split('LN:')[1].strip())
                        else:
                            continue
                    
                    # parse raw SAM line using SAM helper class
                    # we'll pull out the identity and position into a separate array
                    # to make passing the values into the graph function simpler
                    else:
                        sam = SAM(raw_str = l)
                        sam_reads.append(sam)
                        identities.append(sam.identity)
                        coords.append(sam.position)

        except IOError as err:
            print("There was an issue reading your file: {0}".format(err))
            print("Exiting...")
            sys.exit(1)

    return { 'reads': sam_reads, 'coords': coords, 'identities': identities,'len': length, 'ref': ref_name }

# wrapper to call process_sam_file given a directory of SAM files
# will filter for files that end with *.sam extension only, in case
# there are other non-sam files within the directory
def process_sam_file_dir(dir):
    for f in os.listdir(dir):
        if (f.endswith('.sam')):
            file = os.path.join(dir, f)
            print('processing file\t\t{0}'.format(file))
            read = process_sam_file(file)
            graph_sam_read(read, file)

# helper to parse name-mapping json, which maps
# taxon ID, organism name, and NCBI accession number
# SAM files only contain the accession number, but we want the organism name
def get_name_mappings():
    with open('name-mapping.json') as f:
        data = json.load(f)

    name_map = {}

    # convert the json objects to mapped values
    # of acccession = organism name for easy lookup
    for d in data:
        name_map[d['id']] = d['name']

    return name_map

# helper to call graph scatter plot
def graph_sam_read(read, filename):
    # since we could have filenames in different directory paths
    # we only want the base filename without directory to use as prefix
    fname = os.path.basename(filename)
    org_name = name_maps[read['ref']]

    print('drawing graph for\t{0}'.format(fname))
    graph.draw_scatter(prefix = fname, output_dir = out, organism = org_name, positions = read['coords'], identities = read['identities'])

### main ###

# use parser to make the script a little more friendly, versus directly using sys.argv
# only 2 arguments:
#   input: can be a file or a directory where SAM files are located
#   output: directory to store PNG files for FRP, will be created if it doesn't exist yet
parser = argparse.ArgumentParser(description='Create fragment recruitment plots FRP (PNG) given input SAM files')
parser.add_argument('-input', dest='input', help='file or directory path of SAM files', required=True)
parser.add_argument('-output', dest='output', help='output directory to store FRP PNG files', required=True)
args = parser.parse_args()

# create folder for output images, if it doesn't exist yet
if not os.path.exists(args.output):
    os.makedirs(args.output)

out = args.output

# set global name mappings to cross-reference taxon/accession/organism names
name_maps = get_name_mappings()

# process directory of SAM files, will call the directory wrapper helper
if os.path.isdir(args.input):
    process_sam_file_dir(dir = args.input)

# process singular SAM file
else:
    if (args.input.endswith('.sam')):
        r = process_sam_file(args.input)
        graph_sam_read(r, args.input)