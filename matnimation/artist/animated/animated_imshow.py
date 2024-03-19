from matplotlib.axes import Axes
from matplotlib.image import AxesImage
import numpy as np
from matnimation.artist.animated.animated_artist import AnimatedArtist



class AnimatedImshow(AnimatedArtist):
    def __init__(self, name: str, image_data: np.ndarray, extent: list, vis_interval: list[int] = None):    
        """
        Arguments:
        image_data      (list of 2D numpy arrays)    function values f(x,y) on grid for all timesteps len(image_data) = len(time_array)
 

        """            

        super().__init__(name, vis_interval)

        self.image_data = image_data
        self.extent = extent

        self.artist: AxesImage = None
        self.legend_handle = None
    
    def add_to_axes(self, axes: Axes):
        self.artist: AxesImage = axes.imshow(
            self.image_data[0], 
            origin = 'lower', 
            extent = self.extent, 
            vmin = self.image_data[0].min(), 
            vmax = self.image_data[0].max(), 
            zorder = self.zorder
            )
        
        #self.legend_handle: Line2D = Line2D([], [], marker="$\u279B$", markersize = 10, markerfacecolor = self.color, markeredgecolor = self.color, label = self.name, linewidth = 0)
        
    def set_styling_properties(self, **styling):
        if self.artist == None:
            ValueError('For Imshows, the artist must first be added to an axes on the canvas before styling properties can be set.')

        self.artist.set(**styling)

    def update_timestep(self, time_index: int):
        """Set imshow image_data at specific timestep in animation."""

        self.update_visibility(time_index)
        self.artist.set_data(self.image_data[time_index])                         