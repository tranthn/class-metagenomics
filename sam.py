#!/usr/bin/env python3
import sys

"""
SAM Format Basics
- using SAM description courtesy of bowtie2 [http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#sam-output]
- 12 columns:

    1: sample read name
    2: sum of flags
    3: name of reference sequence - mate 1
    4: offset - mate 1
    5: mapping quality
    6: CIGAR
    7: name of reference sequence - mate 2
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

    # convenience for prettier printing if needed
    def __str__(self):
        s = '\nsam-read'
        for i, p in enumerate(self.parts):
            s += '\n\t{0}\t{1}'.format(i, p)

        print('\tmd\t{0}'.format(self.md))
        return s

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