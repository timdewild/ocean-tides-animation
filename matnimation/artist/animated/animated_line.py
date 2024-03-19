from matplotlib.axes import Axes
from matplotlib.lines import Line2D
import numpy as np
from matnimation.artist.animated.animated_artist import AnimatedArtist


class AnimatedLine(AnimatedArtist):

    def __init__(self, name: str, x_data: np.ndarray, y_data: np.ndarray, vis_interval: list[int] = None):
        """
        Arguments:
        x_data      (1D numpy array)        x values of line (assuming they dont change over time) 
        y_data      (2D numpy array)        y values of line (rows) for all timesteps (cols)
        """

        super().__init__(name, vis_interval)
        self.x_data = x_data
        self.y_data = y_data

        self.artist: Line2D = Line2D([], [], zorder = self.zorder, label = self.name)
        self.legend_handle = self.artist

    def get_legend_handle(self):
        return super().get_legend_handle()

    def update_timestep(self, time_index):
        """Set line data at specific timestep in animation."""

        self.update_visibility(time_index)
        self.artist.set_data(self.x_data, self.y_data[:, time_index])