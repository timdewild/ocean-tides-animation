
from matplotlib import colors, pyplot as plt
import numpy as np

import sys
import os

# we add the ~/matnimation directory to be able to import the 'src' module
sys.path.append(os.path.abspath('')) 

from matnimation.artist.static.static_circle import StaticCircle
from matnimation.canvas.single_canvas import SingleCanvas
from matnimation.artist.static.static_text import StaticText
from matnimation.artist.static.static_polygon import StaticPolygon
from matnimation.artist.static.static_scatter import StaticScatter
from matnimation.artist.static.static_quiver import StaticQuiver
from matnimation.tides_forces.tides import Tides




#--- Global constants ---#
radius_earth = 1
ocean_scaling = 1.1
distance_earth_moon = 5

#--- Tidal force due to moon on earth ---#
dth = np.pi/16
theta_vectors = np.arange(0,2*np.pi+dth, dth)

tides = Tides(
    radius_earth = radius_earth,
    ocean_scaling = ocean_scaling,
    distance_earth_moon = distance_earth_moon
)
tides.generate_tidal_bulges()

x_vectors = radius_earth * np.cos(theta_vectors)
y_vectors = radius_earth * np.sin(theta_vectors)

F_tidal_moon_x, F_tidal_moon_y = tides.tidal_force_moon(theta_vectors, tides.t[0], scale = 1)

#--- Tidal bulges due to moon on earth ---#
x_bulge_moon, y_bulge_moon = tides.generate_tidal_bulges(body = 'moon')



#--- Define Canvas ---#

canvas = SingleCanvas(
    (4,4),
    400,
    [],
    [-2, 2, -2, 2],      #[-3, 3, -3, 3] [-2, 6, -4, 4]
    ['$x$','$y$']
)

canvas.set_axis_properties(
    aspect = 'equal', 
    xticklabels = [], 
    yticklabels = [],
    #title = "Frame: Earth Center of Mass"
    )

#--- Define earth and ocean ---#

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

canvas.add_artist(earth)

# ocean = StaticCircle(
#     name = 'Ocean', 
#     radius = ocean_scaling * radius_earth,
#     xy_center = (0., 0.)
# )

ocean = StaticPolygon(
    'ocean',
    x_data = x_bulge_moon[:,0],
    y_data = y_bulge_moon[:,0]
)

ocean.set_styling_properties(
    facecolor = colors.to_rgba('tab:blue', 0.5), 
    zorder = 2
)

canvas.add_artist(ocean)

ocean_no_tides = StaticCircle(
    'no tides',
    radius = ocean_scaling * radius_earth,
    xy_center = (0,0)
)

ocean_no_tides.set_styling_properties(
    linewidth = 0.5,
    linestyle = 'dotted',
    edgecolor = 'k',
    facecolor = 'None'
)

canvas.add_artist(ocean_no_tides, in_legend = True)

#--- ABC forces on earth due to moon ---#
scale = 1.333

y_offset = 0.04

x_vec = np.array([-1, 0, 1])
y_vec = np.array([0, 0, 0])

force_moon_x_vec = np.array([0.5, 1, 1.5])
force_moon_y_vec = np.zeros_like(y_vec)

tidal_force_x_vec = force_moon_x_vec - np.ones_like(force_moon_x_vec)
tidal_force_y_vec = force_moon_y_vec

force_com_x = force_moon_x_vec[1] * np.ones_like(force_moon_x_vec)
force_com_y = force_moon_y_vec[1] * np.ones_like(force_moon_y_vec)

#--- Tidal force at points around equator ---#

tidal_forces_scatter = StaticScatter(
    'tidal forces scatter',
    x_data = x_vectors,
    y_data = y_vectors
)

tidal_forces_scatter.set_styling_properties(
    zorder = 4,
    markersize = 2,
    color  = 'darkblue'
)

canvas.add_artist(tidal_forces_scatter)

tidal_forces_moon = StaticQuiver(
    name = "$\\vec{F}_\\mathrm{tid}^\\mathrm{(moon)}$",
    x_data = x_vectors,
    y_data = y_vectors,
    Fx_data = F_tidal_moon_x,
    Fy_data = F_tidal_moon_y,
    scale = 20,
    scale_units = 'xy', 
    color = 'darkblue',
    width = 0.004 #0.005
)

canvas.add_artist(tidal_forces_moon, in_legend = True)

tidal_forces_moon.set_styling_properties(
    zorder = 4
)

#--- Moon and its orbit ---#

moon_orbit = StaticCircle(
    name = 'Moon orbit',
    radius = distance_earth_moon,
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
    xy_center = (distance_earth_moon,0)
)

moon.set_styling_properties(
    edgecolor = 'darkgrey',
    facecolor = 'lightgrey'
)

#canvas.add_artist(moon_orbit, in_legend = False)
canvas.add_artist(moon)

canvas.construct_legend(ncols = 3, loc = 'lower center', fontsize = 'small')

canvas.save_canvas('scene2/scene2_7.jpg')













