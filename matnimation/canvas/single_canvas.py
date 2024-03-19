from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import numpy as np
from matnimation.artist.base_artist import BaseArtist
from matnimation.canvas.canvas import Canvas

class SingleCanvas(Canvas):
    
    def __init__(self, figsize : tuple, dpi : int, time_array: np.ndarray[float], axis_limits : list, axis_labels : list):
        """
        Initialize Single Canvas.   

        Arguments:
        axis_limits         (list)          1D list with axis limits [xmin, xmax, ymin, ymax]
        axis_labels         (list)          1D list with axis labels ['xlabel', 'ylabel']  
        """

        super().__init__(figsize, dpi, time_array)
        self.axis_limits = [axis_limits]
        self.axis_labels = [axis_labels]
        

        self.fig, self.axs_array = plt.subplots(figsize = self.figsize, squeeze = False, constrained_layout = True)
        self.ax: Axes = self.axs_array[0,0]

        self.set_layout(self.fig, self.axs_array, self.axis_limits, self.axis_labels)

        # set that will contains the Artists' legend handles
        self.legend_handles_collection = set([])

    def set_axis_properties(self, **axis_styling):
        """Set styling properties of canvas, all kwargs of Matplotlib Axis artist can be passed here."""

        self.ax.set(**axis_styling)

    def get_axis(self) -> Axes:
        return self.ax
    
    def add_artist(self, artist: BaseArtist, in_legend = False):
        axes = self.get_axis()
        artist.add_to_axes(axes)
        self._add_artist(artist)

        # if in_legend = True add legend handle to collection
        if in_legend:
            legend_handle = artist.get_legend_handle()
            self.legend_handles_collection.add(legend_handle)

    def construct_legend(self, **legend_styling):
        """
        Construct legend for the single canvas, but only if legend_handles_collection is not empty
        
        **legend_styling contains all the 'other parameters' of the Axes.legend() for styling.
        """

        # if collection of legend handles is not empty, construct legend
        if self.legend_handles_collection:
            axes = self.get_axis()
            legend_handles = self.legend_handles_collection
            self.add_legend(axes, legend_handles, **legend_styling)

