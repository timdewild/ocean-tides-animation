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
from matnimation.artist.static.static_quiver import StaticQuiver
from matnimation.animation.animation import Animation
from matnimation.tides_forces.tides import Tides
from matnimation.artist.animated.animated_circle import AnimatedCircle
from matnimation.helper.helper_functions import HelperFunctions




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

#F_tidal_moon_x, F_tidal_moon_y = tides.tidal_force_moon(theta_vectors, tides.t[0], scale = 1)
#F_tidal_sun_x, F_tidal_sun_y = tides.tidal_force_sun(theta_vectors, tides.t[0], scale = 1)
F_tidal_total_x, F_tidal_total_y = tides.tidal_force_total(theta_vectors, tides.t[0], scale = 1)


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


#--- Tidal bulges due to moon on earth ---#
x_bulge_moon, y_bulge_moon = tides.generate_tidal_bulges( body = 'moon' )
x_bulge_sun, y_bulge_sun = tides.generate_tidal_bulges( body = 'sun' )
x_bulge_total, y_bulge_total = tides.generate_tidal_bulges( body = 'total' )


#--- Define canvas ---#

canvas = SingleCanvas(
    figsize = (4, 4),
    dpi = 400,
    time_array = time_array,
    axis_limits = [-1.75, 1.75, -1.75, 1.75],      #[-3, 3, -3, 3][-2, 6, -4, 4][-2, 2, -2, 2]
    axis_labels = ['$x$','$y$']
)

canvas.set_axis_properties(
    aspect = 'equal', 
    # xticks = np.arange(-17,7,1),
    # yticks = np.arange(-6,6,1),
    xticklabels = [], 
    yticklabels = [],
    #title = "Frame: Co-rotating with Earth around Sun",
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
#     radius = radius_earth * ocean_scaling,
#     xy_center = (0., 0.)
# )

# ocean.set_styling_properties(
#     facecolor = colors.to_rgba('tab:blue', 0.5), 
#     zorder = 2
# )

# canvas.add_artist(ocean)

#--- Ocean with bulges ---#

ocean = StaticPolygon(
    'ocean',
    x_data = x_bulge_total[:,0],
    y_data = y_bulge_total[:,0]
)

ocean.set_styling_properties(
    facecolor = colors.to_rgba('tab:blue', 0.5), 
    zorder = 2
)

canvas.add_artist(ocean)

#--- Ocean no tides ---#

ocean_no_tides = StaticCircle(
    'No Tides',
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

#--- Ocean moon tide only ---#

ocean_moon_tides = StaticPolygon(
    'Moon Only',
    x_data = x_bulge_moon[:,0],
    y_data = y_bulge_moon[:,0]
)

ocean_moon_tides.set_styling_properties(
    linewidth = 0.5,
    linestyle = 'dashed',
    edgecolor = 'k',
    facecolor = 'None'
)

canvas.add_artist(ocean_moon_tides, in_legend = True)


#--- Moon orbit ---#

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

#canvas.add_artist(moon_orbit)

moon = StaticCircle(
    name = 'Moon',
    radius = 0.35,
    xy_center = (5,0)
)

moon.set_styling_properties(
    edgecolor = 'darkgrey',
    facecolor = 'lightgrey',
    zorder = 3
)

canvas.add_artist(moon)

sun = StaticCircle(
    name = 'Sun',
    radius = 2.5,
    xy_center = (-17, 0)
)

sun.set_styling_properties(
    facecolor = colors.to_rgba('tab:orange', 0.4),
    edgecolor = 'tab:orange'
)

canvas.add_artist(sun)

#--- Tidal force at points around equator ---#

# tidal_forces_scatter = StaticScatter(
#     'tidal forces scatter',
#     x_data = x_vectors,
#     y_data = y_vectors
# )

# tidal_forces_scatter.set_styling_properties(
#     zorder = 4,
#     markersize = 2,
#     color  = 'darkblue'
# )

# canvas.add_artist(tidal_forces_scatter)

# #--- Tidal forces moon ---#

# tidal_forces_moon = StaticQuiver(
#     name = "$\\vec{F}_\\mathrm{tid}^\\mathrm{(moon)}$",
#     x_data = x_vectors,
#     y_data = y_vectors,
#     Fx_data = F_tidal_moon_x,
#     Fy_data = F_tidal_moon_y,
#     scale = 20,
#     scale_units = 'xy', 
#     color = 'k',
#     width = 0.004
# )

# canvas.add_artist(tidal_forces_moon, in_legend = True)

# tidal_forces_moon.set_styling_properties(
#     zorder = 4
# )

# #--- Tidal forces sun ---#

# tidal_forces_sun = StaticQuiver(
#     name = "$\\vec{F}_\\mathrm{tid}^\\mathrm{(sun)}$",
#     x_data = x_vectors,
#     y_data = y_vectors,
#     Fx_data = F_tidal_sun_x,
#     Fy_data = F_tidal_sun_y,
#     scale = 20,
#     scale_units = 'xy', 
#     color = 'darkorange',
#     width = 0.004
# )

# canvas.add_artist(tidal_forces_sun, in_legend = True)

# tidal_forces_sun.set_styling_properties(
#     zorder = 4
# )

#--- Tidal forces total ---#

tidal_forces_total = StaticQuiver(
    name = "$\\vec{F}_\\mathrm{tid}^\\mathrm{(total)}$",
    x_data = x_vectors,
    y_data = y_vectors,
    Fx_data = F_tidal_total_x,
    Fy_data = F_tidal_total_y,
    scale = 20,
    scale_units = 'xy', 
    color = 'darkblue',
    width = 0.004
)

#canvas.add_artist(tidal_forces_total, in_legend = True)

# tidal_forces_total.set_styling_properties(
#     zorder = 4
# )

# #--- Moon and its orbit ---#

# moon_orbit = StaticCircle(
#     name = 'Moon orbit',
#     radius = distance_earth_moon,
#     xy_center = (0,0),
# ) 

# moon_orbit.set_styling_properties(
#     edgecolor = 'darkgrey',
#     facecolor = 'None',
#     linewidth = 0.75
# )

# canvas.add_artist(moon_orbit)

# moon = AnimatedCircle(
#     name = 'Moon',
#     radius = 0.35,
#     x_data=x_moon,
#     y_data=y_moon
# )

# moon.set_styling_properties(
#     edgecolor = 'darkgrey',
#     facecolor = 'lightgrey'
# )

# canvas.add_artist(moon_orbit, in_legend = False)
# canvas.add_artist(moon, in_legend = True)

canvas.construct_legend(ncols = 3, loc = 'lower center', fontsize = 'small')

canvas.save_canvas('stem_animation/scene5/scene5_4.jpg')

# animation_scene3 = Animation(canvas, interval = 15)

# animation_scene3.render('stem_animation/scene3/scene3.mp4')