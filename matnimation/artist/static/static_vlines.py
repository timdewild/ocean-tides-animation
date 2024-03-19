from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
import numpy as np
from matnimation.artist.static.static_artist import StaticArtist


class StaticVlines(StaticArtist):
    def __init__(self, name: str, x_data: np.ndarray, y_min: float, y_max: float):    
        """
        Arguments:
        x_data      (1D numpy array)   x values of vlines
        y_min       (float)            y-value of start of vlines
        y_max       (float)            y-value of end of vlines
        """            

        super().__init__(name)

        self.x_data = x_data
        self.y_min = y_min
        self.y_max = y_max

        self.artist: LineCollection = None
        self.legend_handle = None

    def add_to_axes(self, axes: Axes):
        self.artist: LineCollection = axes.vlines(self.x_data, self.y_min, self.y_max)

    def set_styling_properties(self, **styling):
        if self.artist == None:
            ValueError('For Vlines, the artist must first be added to an axes on the canvas before styling properties can be set.')

        self.artist.set(**styling)

    

