import sys
from matplotlib import colors, pyplot as plt
import numpy as np



sys.path.append("/Users/timdewild/Library/CloudStorage/GoogleDrive-t.w.j.de.wild@rug.nl/Mijn Drive/Digital Demos/AnimationClass/src/")

from matnimation.artist.static.static_circle import StaticCircle
from matnimation.artist.animated.animated_polygon import AnimatedPolygon
from matnimation.artist.animated.animated_quiver import AnimatedQuiver
from matnimation.canvas.single_canvas import SingleCanvas
from matnimation.artist.static.static_text import StaticText
from matnimation.artist.static.static_polygon import StaticPolygon
from matnimation.artist.static.static_scatter import StaticScatter
from matnimation.artist.animated.animated_single_scatter import AnimatedSingleScatter
from matnimation.artist.static.static_quiver import StaticQuiver
from matnimation.animation.animation import Animation
from matnimation.tides_forces.tides import Tides
from matnimation.artist.animated.animated_circle import AnimatedCircle
from matnimation.helper.helper_functions import HelperFunctions
from matnimation.canvas.grid_canvas import GridCanvas
from matnimation.artist.static.static_line import StaticLine




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

time_array = tides.get_time_array()

x_vectors = radius_earth * np.cos(theta_vectors)
y_vectors = radius_earth * np.sin(theta_vectors)

F_tidal_moon_x, F_tidal_moon_y = tides.tidal_force_moon(tides.t[0], theta_vectors, scale = 1)

def tidal_force_moon_x(t, theta_array, scale = 1):
    Fx, Fy = tides.tidal_force_moon(t, theta_array, scale = 1)
    return Fx

def tidal_force_moon_y(t, theta_array, scale = 1):
    Fx, Fy = tides.tidal_force_moon(t, theta_array, scale = 1)
    return Fy

data_tidal_force_moon_x = HelperFunctions.func_ab_to_grid(
    tidal_force_moon_x,
    theta_vectors,
    time_array
)

data_tidal_force_moon_y = HelperFunctions.func_ab_to_grid(
    tidal_force_moon_y,
    theta_vectors,
    time_array
)

x_moon, y_moon = tides.get_moon_orbit() 

x_observer, y_observer = tides.generate_observer_equator_trajectory()





#--- Tidal bulges due to moon on earth ---#
x_bulge_moon, y_bulge_moon = tides.generate_tidal_bulges(body = 'moon')


#--- Define canvas ---#

canvas = GridCanvas(
    figsize = (6, 8.5),
    dpi = 400,
    time_array = time_array,
    ncols = 2,
    nrows = 3,
    spans = [[[0,1],[0,1]], [2,[0,1]]],
    axes_keys = ['main', 'tidal variation'],
    axes_limits = [[-6,6,-6,6],[0,30,-0.3,0.5]],
    axes_labels = [['$x$','$y$'], ['$t$ (days)','elevation $h(t)$ (m)']],
    height_ratios = [1, 1, 0.5]
)

canvas.set_axis_properties('main', aspect = 'equal')

canvas.set_axis_properties(
    axes_key = 'main',
    aspect = 'equal', 
    xticklabels = [], 
    yticklabels = [],
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

canvas.add_artist(earth, 'main')

ocean_no_tides = StaticCircle(
    'ocean no tides',
    radius = ocean_scaling * radius_earth,
    xy_center = (0,0)
)

ocean_no_tides.set_styling_properties(
    linewidth = 0.5,
    linestyle = 'dotted',
    edgecolor = 'k',
    facecolor = 'None'
)

canvas.add_artist(ocean_no_tides, 'main')

ocean = AnimatedPolygon(
    'ocean',
    x_data = x_bulge_moon,
    y_data = y_bulge_moon
)

ocean.set_styling_properties(
    facecolor = colors.to_rgba('tab:blue', 0.5), 
    zorder = 2
)

canvas.add_artist(ocean, 'main')


# tidal_forces_moon = AnimatedQuiver(
#     name = "$\\vec{F}_\\mathrm{tid}^\\mathrm{(moon)}$",
#     x_data = x_vectors,
#     y_data = y_vectors,
#     Fx_data = data_tidal_force_moon_x,
#     Fy_data = data_tidal_force_moon_y,
#     scale = 20,
#     scale_units = 'xy', 
#     color = 'darkblue',
#     width = 0.003 #0.005
# )

# #canvas.add_artist(tidal_forces_moon)

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

canvas.add_artist(moon_orbit, 'main')

moon = AnimatedCircle(
    name = 'Moon',
    radius = 0.35,
    x_data = x_moon,
    y_data = y_moon
)

moon.set_styling_properties(
    edgecolor = 'darkgrey',
    facecolor = 'lightgrey'
)

canvas.add_artist(moon, 'main')

#--- Observer stationary on equator ---#
observer = AnimatedSingleScatter(
    name = 'observer',
    x_data = x_observer,
    y_data = y_observer
)

observer.set_styling_properties(
    markersize = 10,
    markerfacecolor = 'tab:red',
    markeredgecolor = 'tab:red'
)

canvas.add_artist(observer, 'main')

#--- Tidal profile due to moon ---#
tidal_profile = StaticLine(
    name = 'tidal profile',
    x_data = time_array,
    y_data = tides.tidal_profile_moon(time_array)
)

tidal_profile.set_styling_properties(
    linewidth = 0.5,
    color = 'tab:blue'
)

canvas.add_artist(tidal_profile, 'tidal variation')

no_tides_line = StaticLine(
    name = 'no tides',
    x_data = [0, 30],
    y_data = [0, 0],
)

no_tides_line.set_styling_properties(
    color = 'k',
    linestyle = 'dotted'
)

canvas.add_artist(no_tides_line, 'tidal variation')

tidal_profile_dot = AnimatedSingleScatter(
    name = 'tidal profile dot',
    x_data = time_array,
    y_data = tides.tidal_profile_moon(time_array)
)

tidal_profile_dot.set_styling_properties(
    markersize = 10,
    markerfacecolor = 'tab:red',
    markeredgecolor = 'tab:red',
    zorder = 4
)

canvas.add_artist(tidal_profile_dot, 'tidal variation')

animation_scene4 = Animation(canvas, interval = 30)

animation_scene4.render('stem_animation/scene4/scene4.mp4')

#canvas.save_canvas('stem_animation/scene4/scene4.jpg')