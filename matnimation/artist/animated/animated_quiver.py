from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.quiver import Quiver
import numpy as np
from matnimation.artist.animated.animated_artist import AnimatedArtist



class AnimatedQuiver(AnimatedArtist):
    def __init__(self, name: str, x_data: np.ndarray, y_data: np.ndarray, Fx_data: np.ndarray, Fy_data: np.ndarray, scale: float = 1., scale_units: str = None, width: float = None, color = 'k', vis_interval: list[int] = None):    
        """
        Arguments:
        x_data      (1D numpy array)    x coordinates of tails of vectors
        y_data      (1D numpy array)    y coordinates of tails of vectors 
        Fx_data     (2D numpy array)    x-component of vectors (rows) at all timesteps (cols) 
        Fy_data     (2D numpy array)    y-component of vectors (rows) at all timesteps (cols)
        scale       (float)             sets scale of vectors
        width       (None or float)     sets with of arrow shaft      
        color       (str or RGBA seq)   arrow color 

        """            

        super().__init__(name, vis_interval)

        self.x_data = x_data
        self.y_data = y_data
        self.Fx_data = Fx_data
        self.Fy_data = Fy_data
        self.scale = scale
        self.scale_units = scale_units
        self.width = width
        self.color = color

        self.artist: Quiver = None
    
    def add_to_axes(self, axes: Axes):
        self.artist: Quiver = axes.quiver(self.x_data, self.y_data, np.zeros_like(self.x_data), np.zeros_like(self.y_data), scale = self.scale, zorder = self.zorder, scale_units = self.scale_units, width = self.width, color = self.color)
        self.legend_handle: Line2D = Line2D([], [], marker="$\u279B$", markersize = 10, markerfacecolor = self.color, markeredgecolor = self.color, label = self.name, linewidth = 0)
        
    def set_styling_properties(self, **styling):
        if self.artist == None:
            ValueError('For Quivers, the artist must first be added to an axes on the canvas before styling properties can be set.')

        self.artist.set(**styling)

    def update_timestep(self, time_index: int):
        """Set quiver vector data at specific timestep in animation."""
        #TO DO: allow for arrow locations to change as well using offsets() method of PathCollection

        self.update_visibility(time_index)
        self.artist.set_UVC(self.Fx_data[:, time_index], self.Fy_data[:, time_index])                         