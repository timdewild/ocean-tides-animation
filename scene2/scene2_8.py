
import sys
from matplotlib import colors, pyplot as plt
import numpy as np


sys.path.append("/Users/timdewild/Library/CloudStorage/GoogleDrive-t.w.j.de.wild@rug.nl/Mijn Drive/Digital Demos/AnimationClass/src/")

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
    [-6, 6, -6, 6],      #[-3, 3, -3, 3] [-2, 6, -4, 4]
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

#--- Gravitational force due to moon on ABC ---#

# force_moon = StaticQuiver(
#     name = '$\\vec{F}_G^\\mathrm{(moon)}$',
#     x_data = x_vec,
#     y_data = y_vec,
#     Fx_data = force_moon_x_vec,
#     Fy_data = force_moon_y_vec, 
#     scale = scale,
#     scale_units = 'xy',
#     width = 0.005, 
#     color = 'darkorange'
# )

# canvas.add_artist(force_moon, in_legend=True)

# force_moon.set_styling_properties(
#     zorder = 4
# )

#--- Subtract gravitational force at B (center of mass) ---#

# force_com_sub = StaticQuiver(
#     name = '$-\\vec{F}_B^\\mathrm{(moon)}$',
#     x_data = x_vec,
#     y_data = y_vec + y_offset,
#     Fx_data = -force_com_x,
#     Fy_data = -force_com_y, 
#     scale = scale,
#     scale_units = 'xy',
#     width = 0.005, 
#     color = 'darkred'
# )

# canvas.add_artist(force_com_sub, in_legend = True)

# force_com_sub.set_styling_properties(
#     zorder = 4
# )

#--- Tidal force at ABC ---#

# tidal_force_moon_ABC = StaticQuiver(
#     name = "$\\vec{F}_\\mathrm{tid}^\\mathrm{(moon)}$",
#     x_data = x_vec,
#     y_data = y_vec,
#     Fx_data = tidal_force_x_vec,
#     Fy_data = tidal_force_y_vec, 
#     scale = 1.333,
#     scale_units = 'xy',
#     width = 0.005, 
#     color = 'darkblue'
# )

# canvas.add_artist(tidal_force_moon_ABC, in_legend = True)

# tidal_force_moon_ABC.set_styling_properties(
#     zorder = 4
# )

#--- ABC points to introduce tidal field

# points_ABC = StaticScatter(
#     name='ABC',
#     x_data = x_vec,
#     y_data = y_vec,

# )

# points_ABC.set_styling_properties(
#     color = 'darkblue',
#     markersize = 5,
#     zorder = 4
# )

# canvas.add_artist(points_ABC)

# for i, label_name in enumerate(['$A$','$B$','$C$']):
#     label = StaticText(name = label_name, xy_center = (x_vec[i],y_vec[i]-0.2))

#     label.set_styling_properties(
#         horizontalalignment = 'center',
#         verticalalignment = 'top',
#         zorder = 4, 
#         fontsize = 8,
#         color = 'k'
#     )

#     canvas.add_artist(label)

#--- Tidal force at points around equator ---#

tidal_forces_scatter = StaticScatter(
    'tidal forces scatter',
    x_data = x_vectors,
    y_data = y_vectors
)

# tidal_forces_scatter.set_styling_properties(
#     zorder = 4,
#     markersize = 2, #5
#     color  = 'darkblue'
# )

#canvas.add_artist(tidal_forces_scatter)

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

#canvas.add_artist(tidal_forces_moon, in_legend = True)

# tidal_forces_moon.set_styling_properties(
#     zorder = 4
# )

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

canvas.add_artist(moon_orbit, in_legend = False)
canvas.add_artist(moon)

canvas.construct_legend(ncols = 3, loc = 'lower center', fontsize = 'small')

canvas.save_canvas('stem_animation/scene2/scene2_8.jpg')












