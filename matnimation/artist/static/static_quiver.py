from matplotlib import colors
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.quiver import Quiver
import numpy as np
from matnimation.artist.static.static_artist import StaticArtist


class StaticQuiver(StaticArtist):
    def __init__(self, name: str, x_data: np.ndarray, y_data: np.ndarray, Fx_data: np.ndarray, Fy_data: np.ndarray, scale: float = 1., scale_units: str = None, width: float = None, color = 'k'):    
        """
        Arguments:
        x_data      (1D numpy array)    x coordinates of tails of vectors
        y_data      (1D numpy array)    y coordinates of tails of vectors 
        Fx_data     (1D numpy array)    x-component of vectors 
        Fy_data     (1D numpy array)    y-component of vectors 
        scale       (float)             sets scale of vectors
        width       (None or float)     sets with of arrow shaft      
        color       (str or RGBA seq)   arrow color      

        """            

        super().__init__(name)

        self.x_data = x_data
        self.y_data = y_data
        self.Fx_data = Fx_data
        self.Fy_data = Fy_data
        self.scale = scale
        self.scale_units = scale_units
        self.width = width
        self.color = color

        self.artist: Quiver = None
    
    def add_to_axes(self, axes: Axes):
        self.artist: Quiver = axes.quiver(self.x_data, self.y_data, self.Fx_data, self.Fy_data, scale = self.scale, zorder = self.zorder, scale_units = self.scale_units, width = self.width, color = self.color)
        self.legend_handle: Line2D = Line2D([], [], marker="$\u279B$", markersize = 10, markerfacecolor = self.color, markeredgecolor = self.color, label = self.name, linewidth = 0)

    def set_styling_properties(self, **styling):
        if self.artist == None:
            raise ValueError('For Quivers, the artist must first be added to (an axes on) the canvas before styling properties can be set.')

        self.artist.set(**styling)

    