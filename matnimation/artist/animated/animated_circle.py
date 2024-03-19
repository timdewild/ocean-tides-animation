from matplotlib.axes import Axes
import numpy as np
from matnimation.artist.animated.animated_artist import AnimatedArtist


from matplotlib import patches


class AnimatedCircle(AnimatedArtist):

    def __init__(self, name: str, radius: float, x_data: np.ndarray, y_data: np.ndarray, vis_interval: list[int] = None):
        """
        Arguments:
        radius      (float or int)  radius of circle
        x_data      (1D np array)   x values of center for all timesteps
        y_data      (1D np array)   y values of center for all timesteps
        """

        super().__init__(name, vis_interval)
        self.radius = radius
        self.x_data = x_data
        self.y_data = y_data

        

        self.artist: patches.Circle = patches.Circle((0,0), radius = self.radius, zorder = self.zorder)

    def get_legend_handle(self):
        return super().get_legend_handle()

    def update_timestep(self, time_index):
        """Set center coordinates of patch at specific timestep in animation."""

        self.update_visibility(time_index)
        xy_data = (self.x_data[time_index], self.y_data[time_index])
        self.artist.set_center(xy_data)

    