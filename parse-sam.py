#!/usr/bin/env python3
import sys
import os
from sam import SAM

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

                    # skip header lines, except for SN/LN
                    if (l.startswith('@')):
                        if 'LN:' in l or 'SN:' in l:
                            # splits header into 3 parts: @SQ, SN, LN
                            parts = l.split('\t')
                            ref_name = parts[1].split('SN:')[1]
                            length = int(parts[2].split('LN:')[1].strip())
                        else:
                            continue
                    else:
                        sam = SAM(raw_str = l)
                        sam_reads.append(sam)

        except IOError as err:
            print("There was an issue reading your file: {0}".format(err))
            print("Exiting...")
            sys.exit(1)

    return { 'reads': sam_reads, 'len': length, 'ref': ref_name }

def process_sam_file_dir(dir):
    reads = []
    for f in os.listdir(dir):
        file = os.path.join(dir, f)
        reads.append(process_sam_file(file))

    return reads

### main ###
if (len(sys.argv) > 1):
    sam_reads = process_sam_file_dir(dir = sys.argv[1])
    for r in sam_reads:
        print(r['ref'])
        print(r['len'])
        print()
else:
    print('No file argument was passed, exiting...')
    sys.exit(1)