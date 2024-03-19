from matplotlib.lines import Line2D
from matnimation.artist.animated.animated_artist import AnimatedArtist
import numpy as np

class AnimatedSingleScatter(AnimatedArtist):

    def __init__(self, name: str, x_data: np.ndarray, y_data: np.ndarray, vis_interval: list[int] = None):
        """
        Animated single scatter.

        Scatter is interpreted here as a matplotlib Line2D object with no line (linewidth = 0) but with specified markers (marker = '.') at all data points. 

        Arguments:
        x_data      (1D array)  array with x coordinate of single scatter at all timesteps
        y_data      (1D array)  array with y coordinate of single scatter at all timesteps
                                        

        """
        super().__init__(name, vis_interval)

        # check if x_data and y_data correspond to a single scatter point
        if x_data.ndim != 1 or y_data.ndim != 1:
            raise ValueError('Both x_data and y_data should be 1D arrays for a single scatter.')

        self.x_data = x_data
        self.y_data = y_data

        #Here scatter is a line with no linewidth and dots as markers at vertices
        self.artist: Line2D = Line2D([], [], linewidth = 0, marker = '.', markersize = 10, label = self.name) 

        #Create handle for legend
        self.legend_handle = self.artist
    
    # def get_legend_handle(self):
    #     return self.legend_handle
        
    def update_timestep(self, time_index: int):
        """Set coordinates of scatters at specific timestep in animation."""


        self.update_visibility(time_index)
        self.artist.set_data(self.x_data[time_index], self.y_data[time_index])

    
        
