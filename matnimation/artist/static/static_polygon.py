from matplotlib.axes import Axes
from matnimation.artist.static.static_artist import StaticArtist
import numpy as np
from matplotlib import patches


class StaticPolygon(StaticArtist):

    def __init__(self, name: str, x_data: np.ndarray, y_data: np.ndarray):
        """
        Arguments:
        x_data      (1D np array)   x values of polygon 
        y_data      (1D np array)   y values of polygon
        """

        super().__init__(name)
        self.x_data = x_data
        self.y_data = y_data
        

        self.artist: patches.Polygon = patches.Polygon(np.column_stack([self.x_data, self.y_data]), zorder = self.zorder, closed = True, label = self.name)
        self.legend_handle = self.artist
    