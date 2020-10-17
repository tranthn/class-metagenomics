#!/usr/bin/env python3
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib

# draws scatter plot representing our fragment recruitment plot
#
# arguments
#   - ref_name: name of reference genome (e.g. NC_1111)
#   - ref_genome_len: length of reference genome, to be used for x-axis limit
#   - positions: flat 1-d array of starting coordinates for aligned sequences from our sample
#   - identities: flat 1-d array of identities matching above position coordinates
#
# returns
#   - nothing, will save plot to output PNG
def draw_scatter(ref_name, ref_genome_len, positions, identities):
    x = positions
    y = identities
    colors = np.random.rand(len(x))
    area = 4

    ## draw actual scatter plot
    plt.scatter(x, y, s = area, c = colors, alpha = 0.5)
    
    ## set axes
    plt.xlim(0, ref_genome_len)
    plt.ylim(0, 1.1)
    plt.grid()

    # save to output, rather than drawing inline
    plt.savefig('{0}.png'.format(ref_name), format='png')