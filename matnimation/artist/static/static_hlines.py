from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
import numpy as np
from matnimation.artist.static.static_artist import StaticArtist


class StaticHlines(StaticArtist):
    def __init__(self, name: str, y_data: np.ndarray, x_min: float, x_max: float):    
        """
        Arguments:
        y_data      (1D numpy array)   y values of hlines
        x_min       (float)            x-value of start of hlines
        x_max       (float)            x-value of end of hlines
        """            

        super().__init__(name)

        self.y_data = y_data
        self.x_min = x_min
        self.x_max = x_max

        self.artist: LineCollection = None
        self.legend_handle = None

    def add_to_axes(self, axes: Axes):
        self.artist: LineCollection = axes.hlines(self.y_data, self.x_min, self.x_max)

    def set_styling_properties(self, **styling):
        if self.artist == None:
            ValueError('For Vlines, the artist must first be added to an axes on the canvas before styling properties can be set.')

        self.artist.set(**styling)

    

