#!/usr/bin/env python3
import sys
import re

"""
SAM Format Basics
- using SAM description courtesy of bowtie2 [http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#sam-output]
- 12 columns:

    1: name of aligned read from sample
    2: sum of flags
    3: name of matched reference sequence - mate 1
    4: offset - mate 1
    5: mapping quality
    6: CIGAR
    7: name of matched reference sequence - mate 2
    8: offset - mate 2
    9: fragment length
   10: read sequence
   11: read qualities
   12: optional fields (contains what we will want for our fragment recruitment plot)
        - XM:i:<N> - number of mismatches
        - MD:Z:<S> - represents mismatches relative to reference genome, only present for aligned reads
             - will be main piece we can use for identity
             - example: 58G18A22
                - 58 matched bases
                - 1 mismatch with a G (position 59)
                - 18 matched bases
                - 1 mismatch with an A (position 78)
                - 22 matched bases
                - total = 100 bases

        ...and more

"""

# calculates percent identity given an MD string from SAM format
# arguments:
#   - md: MD string per SAM format, example below:
# 
# str. MD:Z:19A18A5T54G0
# expl: 19 matches | 1 mismatch | 18 matches | 1 mismatch | 5 matches | 1 mismatch | 54 matches | 1 mismatch | 0 dummy separator
#
# returns:
#   - float, percent identity (matches over total bases, including deletions)
def identity(md):
    s = md
    tokens = re.split(r'(\d+)', s)
    total = 0
    matches = 0

    # handle scenarios where MD may be empty or None
    if md == '' or md is None:
        return 0.0

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

### parse line string representing SAM alignment
class SAM():
    def __init__(self, raw_str = ""):
        self.raw_str = raw_str

        # hold the tokenized parts of the SAM string
        # should be 12 parts representing the columns for SAM string 
        self.parts = []
        
        # mismatch representation, which we will use for identity calculate (see above format comments for more)
        self.md = ''

        # process raw string into parts
        self.split_str(raw_str)

        # process MD string to set identity
        self.identity = identity(self.md)

    # default override for string printing
    # prints all available attributes and identity
    def __str__(self):
        s = '\nsam-read'
        for i, p in enumerate(self.parts):
            s += '\n\t{0}\t{1}'.format(i, p)

        print('\tmd\t{0}'.format(self.md))
        print('\tidentity\t{:.3%}'.format(self.identity))
        return s

    def get_plot_objects(self):
        obj = {
            
            # col 4 represents position for read 1, -1 for 0-indexing
            'offset1': self.parts[3],

            # col 8 represents offset for read 2, -1 for 0-indexing
            'offset2': self.parts[7],
            'md': self.md,
            'identity': self.identity
        }

        return obj

    # splits maximimum of 11 times on tab-separated line
    # see top of file for quick breakdown of columns
    def split_str(self, s):
        self.parts = s.split('\t', 11)

        # tokenizes option values into relevant parts
        # while there should be 12 columns for the aligned/filtered SAM files
        # we will add a check just in case, to prevent out of bounds
        if (len(self.parts) == 12):
            options_col = self.parts[11]
            opt_parts = options_col.split('\t')

            # further tokenize the option column and find the MD value
            for o in opt_parts:
                if (o.find('MD') > -1):
                    self.md = o