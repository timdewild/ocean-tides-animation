from matnimation.artist.static.static_artist import StaticArtist
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
import numpy as np
from matnimation.artist.static.static_artist import StaticArtist


class StaticScatter(StaticArtist):
    def __init__(self, name: str, x_data: np.ndarray, y_data: np.ndarray):    
        """
        Arguments:
        x_data      (1D numpy array)   x values of scatters
        y_data      (1D numpy array)   y values of scatters
        """            

        super().__init__(name)

        self.x_data = x_data
        self.y_data = y_data

        self.artist: Line2D = Line2D(self.x_data, self.y_data, linewidth = 0, marker = '.', markersize = 10, label = self.name) 
        self.legend_handle = self.artist

    




   