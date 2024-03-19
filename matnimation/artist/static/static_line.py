from matplotlib.axes import Axes
from matplotlib.lines import Line2D
import numpy as np
from matnimation.artist.static.static_artist import StaticArtist


class StaticLine(StaticArtist):
    def __init__(self, name: str, x_data: np.ndarray, y_data: np.ndarray):    
        """
        Arguments:
        x_data      (1D numpy array)   x values of line
        y_data      (1D numpy array)   y values of line
        """            

        super().__init__(name)

        self.x_data = x_data
        self.y_data = y_data

        self.artist: Line2D = Line2D(x_data, y_data, zorder = self.zorder, label = self.name)
        self.legend_handle = self.artist

    

