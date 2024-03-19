from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import numpy as np
from matnimation.artist.base_artist import BaseArtist
from matnimation.canvas.canvas import Canvas

class MultiCanvas(Canvas):

    def __init__(
            self, 
            figsize : tuple, 
            dpi : int, 
            time_array: np.ndarray[float],
            nrows: int, 
            ncols: int, 
            axes_limits: list,          
            axes_labels: list,  
            shared_x = False,
            shared_y = False
            ):
        """
        Initialize Multi Canvas.   

        Arguments:
        nrows               (int)           number of rows with subplots
        ncols               (int)           number of rows with subplots
        axis_limits         (list)          2D list with axes limits [[xmin, xmax, ymin, ymax], ...]
        axis_labels         (list)          2D list with axes labels [['xlabel', 'ylabel'], ...]
        *args
        shared_x            (bool)          x axis of subplots shared
        shared_y            (bool)          y axis of subplots shared


        In lists 'axis_limits' and 'axis_labels', the first sublist corresponds to the first axis (top-left). 
        The order of the axes is left-to-right and top-to-bottom of their position in the total layout.
        """

        super().__init__(figsize, dpi, time_array)

        self.nrows = nrows
        self.ncols = ncols
        self.axes_limits = axes_limits
        self.axes_labels = axes_labels
        self.shared_x = shared_x
        self.shared_y = shared_y

        if (self.nrows == 1) and (self.ncols == 1):
            raise ValueError('You specified a canvas with only one plot (ncols = nrows = 1), use SingleCanvas instead.')  
        
        self.fig, self.axs_array = plt.subplots(
            nrows = self.nrows, 
            ncols = self.ncols, 
            constrained_layout = True, 
            squeeze = False, 
            sharex = self.shared_x, 
            sharey = self.shared_y
            )
        
        self.set_layout(self.fig, self.axs_array, self.axes_limits, self.axes_labels)

        # 2D list (nrows, ncols) that contains sets for legend_handles for all subplots
        self.legend_handles_collection = [[set() for j in range(self.ncols)] for i in range(self.nrows)]

    def set_axis_properties(self, row: int, col: int, **axis_styling):
        """Set styling properties of axis located at [row, col] in the grid, all kwargs of Matplotlib Axis artist can be passed here."""

        ax = self.get_axis(row, col)
        ax.set(**axis_styling)

    def get_axis(self, row: int, col: int) -> Axes:
        """Get Axis object of subplot located at (row, col)."""
        
        ax = self.axs_array[row, col]
        return ax
    
    def add_artist(self, artist: BaseArtist, row: int, col: int, in_legend = False):
        axes = self.get_axis(row, col)
        artist.add_to_axes(axes)
        self._add_artist(artist)

        if in_legend:
            legend_handle = artist.get_legend_handle()
            self.legend_handles_collection[row][col].add(legend_handle)

    def construct_legend(self, row: int, col: int,  **legend_styling):
        """
        Construct legend for the axes (row, col), but only if legend_handles_collection for the axes is not empty.
        
        **legend_styling contains all the 'other parameters' of the Axes.legend() for styling.
        """
        
        if self.legend_handles_collection[row][col]:
            legend_handles = self.legend_handles_collection[row][col]
            axes = self.get_axis(row, col)
            self.add_legend(axes, legend_handles)

        