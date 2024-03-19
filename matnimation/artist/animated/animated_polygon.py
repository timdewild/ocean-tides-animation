from matplotlib.axes import Axes
from matnimation.artist.animated.animated_artist import AnimatedArtist
import numpy as np
from matplotlib import patches


class AnimatedPolygon(AnimatedArtist):

    def __init__(self, name: str, x_data: np.ndarray, y_data: np.ndarray, vis_interval: list[int] = None):
        """
        Arguments:
        x_data      (2D np array)   x values of polygon (rows) for all timesteps (cols)
        y_data      (2D np array)   y values of polygon (rows) for all timesteps (cols)
        """

        super().__init__(name, vis_interval)
        self.x_data = x_data
        self.y_data = y_data
        

        self.artist: patches.Polygon = patches.Polygon(np.array([[0,0],[1,0],[1,1],[0,1]]), zorder = self.zorder, closed = True, label = self.name)
        self.legend_handle = self.artist

    def update_timestep(self, time_index):
        """Set polygon coordinates at specific timestep in animation."""

        self.update_visibility(time_index)
        xy_data = np.column_stack([self.x_data[:,time_index], self.y_data[:,time_index]])
        self.artist.set_xy(xy_data)