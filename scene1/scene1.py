from matplotlib import colors
import numpy as np

import sys
import os

# we add the ~/matnimation directory to be able to import the 'src' module
sys.path.append(os.path.abspath('')) 

from matnimation.artist.static.static_circle import StaticCircle
from matnimation.canvas.single_canvas import SingleCanvas



canvas = SingleCanvas(
    (4,4),
    400,
    [],
    [-2, 2, -2, 2],
    ['$x$','$y$']
)

canvas.set_axis_properties(
    aspect = 'equal', 
    xticks = np.arange(-2,3,1),
    yticks = np.arange(-2,3,1),
    xticklabels = [], 
    yticklabels = []
    )


earth = StaticCircle(
    name = 'Earth (equator slice)', 
    radius = 1.,
    xy_center = (0., 0.)
)

earth.set_styling_properties(
    facecolor = 'seagreen',
    edgecolor = 'darkgreen',
    zorder = 3
    )

ocean = StaticCircle(
    name = 'Ocean', 
    radius = 1.1,
    xy_center = (0., 0.)
)

ocean.set_styling_properties(
    facecolor = colors.to_rgba('tab:blue', 0.5), 
    zorder = 2
)

canvas.add_artist(earth, in_legend=True)
canvas.add_artist(ocean, in_legend=True)

canvas.construct_legend(ncols = 2, loc = 'lower center', fontsize = 'small')


canvas.save_canvas('scene1/scene1.jpg')


