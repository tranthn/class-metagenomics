#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plot
import matplotlib

# draws scatter plot representing our fragment recruitment plot
#
# arguments
#   - prefix: name to use for output graph file, which will be <current directory>/out/prefix.png
#   - positions: flat 1-d array of starting coordinates for aligned sequences from our sample
#   - identities: flat 1-d array of identities matching above position coordinates
#
# returns
#   - nothing, will save plot to output PNG
def draw_scatter(prefix, organism, positions, identities):
    def f(x):
        return x / 1000000

    x = np.array(positions)
    x = np.array([f(xi) for xi in x])
    y = np.array(identities)

    colors = np.random.rand(len(x))
    area = 3

    ## draw actual scatter plot
    plot.scatter(x, y, s = area, c = colors, alpha = 0.5, marker = '.')

    ## set labels for axes
    plot.ylabel('% identity')
    plot.xlabel('position [Mbp]')
    plot.title(organism)

    ## set axes boundaries
    ## add a bit of buffer to percent identity for min and max for easier visualization
    plot.ylim(y.min() - 0.1, 1.0)
    plot.grid()

    file_name = 'out/' + prefix + '.graph.png'
    print('writing graph out to {0}'.format(file_name))

    # save to output, rather than drawing inline
    plot.savefig('{0}'.format(file_name), format='png')