import sys
from matplotlib import colors
import numpy as np

sys.path.append("/Users/timdewild/Library/CloudStorage/GoogleDrive-t.w.j.de.wild@rug.nl/Mijn Drive/Digital Demos/AnimationClass/src/")

from matnimation.artist.static.static_circle import StaticCircle
from matnimation.canvas.single_canvas import SingleCanvas
from matnimation.artist.static.static_text import StaticText

radius_earth = 1
ocean_scaling = 1.1

canvas = SingleCanvas(
    (4,4),
    400,
    [],
    [-2, 6, -4, 4],
    ['$x$','$y$']
)

canvas.set_axis_properties(
    aspect = 'equal', 
    xticklabels = [], 
    yticklabels = []
    )


earth = StaticCircle(
    name = 'Earth (equator slice)', 
    radius = radius_earth,
    xy_center = (0., 0.)
)

earth.set_styling_properties(
    facecolor = 'seagreen',
    edgecolor = 'darkgreen',
    linewidth = 0.5,
    zorder = 3
    )

ocean = StaticCircle(
    name = 'Ocean', 
    radius = radius_earth * ocean_scaling,
    xy_center = (0., 0.)
)

ocean.set_styling_properties(
    facecolor = colors.to_rgba('tab:blue', 0.5), 
    zorder = 2
)

moon_orbit = StaticCircle(
    name = 'Moon orbit',
    radius = 5,
    xy_center = (0,0),
) 

moon_orbit.set_styling_properties(
    edgecolor = 'darkgrey',
    facecolor = 'None',
    linewidth = 0.75
)

moon = StaticCircle(
    name = 'Moon',
    radius = 0.35,
    xy_center = (5,0)
)

moon.set_styling_properties(
    edgecolor = 'darkgrey',
    facecolor = 'lightgrey'
)

canvas.add_artist(earth)
canvas.add_artist(ocean)

#canvas.add_artist(moon_orbit, in_legend = False)
canvas.add_artist(moon, in_legend = True)

canvas.construct_legend(ncols = 2, loc = 'lower center', fontsize = 'small')


canvas.save_canvas('stem_animation/scene2/scene2_1.jpg')


