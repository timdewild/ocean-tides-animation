import numpy as np
from matnimation.artist.animated.animated_artist import AnimatedArtist
from matplotlib import patches


class AnimatedEllipse(AnimatedArtist):

    def __init__(
            self, 
            name: str, 
            width: float,
            height: float,
            x_data: np.ndarray, 
            y_data: np.ndarray, 
            vis_interval: list[int] = None, 
            width_data: np.ndarray = None, 
            height_data: np.ndarray = None
            ):
        """
        Arguments:
        height      (float or int)  height of ellipse
        width       (float or int)  width of ellipse
        x_data      (1D np array)   x values of center for all timesteps
        y_data      (1D np array)   y values of center for all timesteps
        width_data  (1D np array)   width of ellipse at all timesteps 
        height_data (1D np array)   height of ellipse at all timesteps
        """

        super().__init__(name, vis_interval)
        self.width = width
        self.height = height
        self.x_data = x_data
        self.y_data = y_data
        self.width_data = width_data
        self.height_data = height_data

        

        self.artist: patches.Ellipse = patches.Ellipse((0, 0), width = self.width, height = self.width)

    def get_legend_handle(self):
        return super().get_legend_handle()

    def update_timestep(self, time_index):
        """Set center coordinates of patch at specific timestep in animation."""

        self.update_visibility(time_index)

        xy_data = (self.x_data[time_index], self.y_data[time_index])
        self.artist.set_center(xy_data)

        if self.width_data is not None:
            width = self.width_data[time_index]
            self.artist.set_width(width)
        
        if self.height_data is not None:
            height = self.height_data[time_index]
            self.artist.set_height(height)