#!/usr/bin/env python3
import sys
import json
import os
from sam import SAM
import graph

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
def process_sam_file_dir(dir):
    reads = []
    for f in os.listdir(dir):
        if (f.endswith('.sam')):
            file = os.path.join(dir, f)
            print('processing:\t{0}'.format(file))
            reads.append(process_sam_file(file))

    return reads

# helper to parse name-mapping json, which maps
# taxon ID x organism name x NCBI accession number
# SAM files contain the accession number, but we want the organism name
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
    org_name = name_maps[r['ref']]

    print('drawing graph for {0}...'.format(fname))
    graph.draw_scatter(prefix = fname, organism = org_name, positions = read['coords'], identities = read['identities'])

### main ###
global name_maps

if (len(sys.argv) > 1):
    arg = sys.argv[1]
    name_maps = get_name_mappings()

    # process directory of SAM files, will call the directory wrapper helper
    if os.path.isdir(arg):
        sam_reads = process_sam_file_dir(dir = sys.argv[1])
        for r in sam_reads:
            graph_sam_read(r, arg)

    # process singular SAM file
    else:
        if (arg.endswith('.sam')):
            r = process_sam_file(arg)
            graph_sam_read(r, arg)

    print()
else:
    print('No file argument was passed, exiting...')
    sys.exit(1)