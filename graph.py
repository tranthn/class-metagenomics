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
def draw_scatter(prefix, output_dir, organism, positions, identities):
    # helper to scale down coordinate values, represented as Mbp
    def as_mbp(x):
        return x / 1000000

    # convert arrays to numpy arrays to allow use of some convenience methods
    x = np.array(positions)
    x = np.array([as_mbp(xi) for xi in x])
    y = np.array(identities)

    colors = np.random.rand(len(x))
    area = 3

    # draw actual scatter plot
    # use the '.' / period marker to reduce the density of the points on graph
    plot.scatter(x, y, s = area, c = colors, alpha = 0.5, marker = '.')

    # set labels for axes
    plot.ylabel('% identity')
    plot.xlabel('position [Mbp]')

    # determine which algorithm was used, so we can indicate in graph
    if ('bwa' in prefix):
        plot.title(organism + ' [BWA]')
    else:
        plot.title(organism + ' [Bowtie2]')

    # set axes boundaries
    # add a bit of buffer to percent identity for min and max for easier visualization
    plot.ylim(y.min() - 0.1, 1.0)
    plot.grid()

    # keep all PNGs contained in specified output directory
    file_name = output_dir + '/' + prefix + '.graph.png'
    print('saving graph to\t\t{0}'.format(file_name))
    print()

    # save to output, rather than drawing inline
    plot.savefig('{0}'.format(file_name), format='png')