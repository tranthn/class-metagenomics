#!/usr/bin/env python3
import sys
import re
from sam import SAM

# calculates percent identity given an MD string from SAM format
# arguments:
#   - md: MD string per SAM format, example below:
# 
# str. MD:Z:19A18A5T54G0
# expl: 19 matches | 1 mismatch | 18 matches | 1 mismatch | 5 matches | 1 mismatch | 54 matches | 1 mismatch | 0 dummy separator
#
# returns:
#   - percent identity (matches over total bases, including deletions)
def identity(md):
    s = md
    tokens = re.split(r'(\d+)', s)
    total = 0
    matches = 0

    for t in tokens:

        # ignore MD:Z
        if t.startswith('MD'):
            continue        

        elif t.isdigit():
            matches += int(t)
            total += int(t)
        
        elif t.startswith('^'):
            dels = t.split('^')[1]
            total += len(dels)
        
        # alphabetic characters representing mismatches
        # we're not tracking mismatches independently, just add to total
        elif t.isalpha():
            total += len(t)
    
    return round(matches / total, 3)

# parses filtered SAM file that only contains aligned reads
#
# arguments:
#   - input: file path to SAM file
#
# returns
#   - list of parsed SAM reads objects, using imported SAM class
def process_sam_file(input):
    sam_reads = []

    if input != "":
        try:
            with open(input, 'r') as inp:
                for l in inp:

                    # skip header lines
                    if (l.startswith('@')):
                        continue
                    else:
                        sam = SAM(raw_str = l)
                        sam_reads.append(sam)

        except IOError as err:
            print("There was an issue reading your file: {0}".format(err))
            print("Exiting...")
            sys.exit(1)

    return sam_reads

### main ###
if (len(sys.argv) > 1):
    sam_reads = process_sam_file(input = sys.argv[1])
    for r in sam_reads:
        i = identity(r.md)
        print('\n{0}\nidentity:\t{1}'.format(r.md, i))
else:
    print('No file argument was passed, exiting...')
    sys.exit(1)