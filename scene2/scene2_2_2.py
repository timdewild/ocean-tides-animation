import sys
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
from matnimation.artist.animated.animated_ellipse import AnimatedEllipse
from matnimation.animation.animation import Animation
from matnimation.artist.animated.animated_circle import AnimatedCircle




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

Nt = 30
t_array = np.linspace(0,1,Nt)

dx = 0.15
dy = 0.04 


#--- Define Canvas ---#

canvas = SingleCanvas(
    (4.5,4),
    400,
    t_array,
    [-2, 2, -2, 2],      #[-3, 3, -3, 3][-2, 6, -4, 4]
    ['$x$','$y$']
)

canvas.set_axis_properties(
    aspect = 'equal', 
    xticklabels = [], 
    yticklabels = [],
    title = "Frame: Earth Center of Mass"
    )

#--- Define earth and ocean ---#

earth = StaticCircle(
    name = 'Earth (equator slice)', 
    radius = radius_earth,
    xy_center = (0,0)
)

earth.set_styling_properties(
    facecolor = 'seagreen',
    edgecolor = 'darkgreen',
    linewidth = 0.5,
    zorder = 3
    )

canvas.add_artist(earth)

ocean = AnimatedEllipse(
    name = 'Ocean', 
    width = 2 * ocean_scaling * radius_earth,
    height = 2 * ocean_scaling * radius_earth,
    x_data = np.zeros(Nt),
    y_data = np.zeros(Nt), 
    width_data = np.linspace(2 * ocean_scaling * radius_earth, 2 * ocean_scaling * radius_earth + 2 * dx, Nt),
    height_data = np.linspace(2 * ocean_scaling * radius_earth, 2 * ocean_scaling * radius_earth - 2 * dy, Nt)
)

# ocean = StaticPolygon(
#     'ocean',
#     x_data = x_bulge_moon[:,0],
#     y_data = y_bulge_moon[:,0]
# )

ocean.set_styling_properties(
    facecolor = colors.to_rgba('tab:blue', 0.5), 
    zorder = 2
)

canvas.add_artist(ocean)

canvas.construct_legend(ncols = 3, loc = 'lower center', fontsize = 'small')

#canvas.save_canvas('stem_animation/scene2/scene2_2_1.jpg')

animation = Animation(canvas)
animation.render('scene2/scene2_2_2.mp4')