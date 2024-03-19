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
    [-3, 3, -3, 3],      #[-3, 3, -3, 3] [-2, 6, -4, 4]
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

ocean = StaticCircle(
    name = 'Ocean', 
    radius = ocean_scaling * radius_earth,
    xy_center = (0., 0.)
)

ocean.set_styling_properties(
    facecolor = colors.to_rgba('tab:blue', 0.5), 
    zorder = 2
)

canvas.add_artist(ocean)

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

#--- Tidal force at ABC ---#

tidal_force_moon_ABC = StaticQuiver(
    name = "$\\vec{F}_\\mathrm{tid}^\\mathrm{(moon)}$",
    x_data = x_vec,
    y_data = y_vec,
    Fx_data = tidal_force_x_vec,
    Fy_data = tidal_force_y_vec, 
    scale = 1.333,
    scale_units = 'xy',
    width = 0.005, 
    color = 'darkblue'
)

canvas.add_artist(tidal_force_moon_ABC, in_legend = True)

tidal_force_moon_ABC.set_styling_properties(
    zorder = 4
)

#--- ABC points to introduce tidal field

points_ABC = StaticScatter(
    name='ABC',
    x_data = x_vec,
    y_data = y_vec,

)

points_ABC.set_styling_properties(
    color = 'darkblue',
    markersize = 5,
    zorder = 4
)

canvas.add_artist(points_ABC)

for i, label_name in enumerate(['$A$','$B$','$C$']):
    label = StaticText(name = label_name, xy_center = (x_vec[i],y_vec[i]-0.2))

    label.set_styling_properties(
        horizontalalignment = 'center',
        verticalalignment = 'top',
        zorder = 4, 
        fontsize = 8,
        color = 'k'
    )

    canvas.add_artist(label)

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

canvas.save_canvas('scene2/scene2_4.jpg')