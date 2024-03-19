from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import numpy as np
from matnimation.artist.base_artist import BaseArtist
from matnimation.canvas.canvas import Canvas

class CustomCanvas(Canvas):
    
    def __init__(
            self, 
            figsize : tuple, 
            dpi : int, 
            time_array: np.ndarray[float],
            mosaic: list,
            axes_limits: list,          
            axes_labels: list, 
            shared_x = False,
            shared_y = False,
            width_ratios = None, 
            height_ratios = None,
            gridspec_kw = None
            ):
        """
        Initialize Custom Canvas.   

        Arguments:
        mosaic              (list)          list with sublists specifying mosaic/shape of Axes, 
                                            e.g. [['Axes 1', 'Axes 1'],['Axes 2', 'Axes 3']] 
                                            Axes 1 spans entire first row, 
                                            Axes 2 (3) spans second row and first (second) column
        axes_limits         (list)          2D list with axes limits [[xmin, xmax, ymin, ymax], ...]
        axes_labels         (list)          2D list with axes labels [['xlabel', 'ylabel'], ...]  
        *args
        shared_x            (bool)          x axis of subplots shared
        shared_y            (bool)          y axis of subplots shared

        In lists 'axis_limits' and 'axis_labels', the first sublist corresponds to the first axis (top-left). 
        In these lists, the lengthequal number of axes in mosaic.
        The order of the axes in the lists is left-to-right and top-to-bottom of their position in the total layout.
        """

        super().__init__(figsize, dpi, time_array)
        
        self.mosaic = mosaic
        self.axes_limits = axes_limits
        self.axes_labels = axes_labels

        self.shared_x = shared_x
        self.shared_y = shared_y
        self.width_ratios = width_ratios
        self.height_ratios = height_ratios
        self.gridspec_kw = gridspec_kw

        self.fig, self.axs_dict = plt.subplot_mosaic(
            self.mosaic, 
            width_ratios = self.width_ratios, 
            height_ratios = self.height_ratios,
            sharex = self.shared_x,
            sharey = self.shared_y,
            constrained_layout = True, 
            gridspec_kw = self.gridspec_kw
            )
        
        # transform dict with axes to 1D numpy array
        self.axs_array = np.array(list(self.axs_dict.values()))

        self.set_layout(self.fig, self.axs_array, self.axes_limits, self.axes_labels)

        self.axs_keys = self.axs_dict.keys()
        self.legend_handles_collection = {axis_key:set() for axis_key in self.axs_keys}

    def get_axis(self, axis_key: str) -> Axes:
        """Get Axis object of subplot with axis_key."""
        
        ax = self.axs_dict[axis_key]
        return ax 

    def set_axis_properties(self, axis_key: str, **axis_styling):
        """Set styling properties of axis with axis_key, all kwargs of Matplotlib Axis artist can be passed here."""

        ax = self.get_axis(axis_key)
        ax.set(**axis_styling)
    
    def add_artist(self, artist: BaseArtist, axes_key: str, in_legend = False):
        axes = self.get_axis(axes_key)
        artist.add_to_axes(axes)
        self._add_artist(artist)

        if in_legend:
            legend_handle = artist.get_legend_handle()
            self.legend_handles_collection[axes_key].add(legend_handle)

    def construct_legend(self, axes_key: str, **legend_styling):
        """
        Construct legend for the axes with axes_key, but only if legend_handles_collection for the axes is not empty.
        
        **legend_styling contains all the 'other parameters' of the Axes.legend() for styling.
        """

        if self.legend_handles_collection[axes_key]:
            legend_handles = self.legend_handles_collection[axes_key]
            axes = self.get_axis(axes_key)
            self.add_legend(axes, legend_handles, **legend_styling)


            
