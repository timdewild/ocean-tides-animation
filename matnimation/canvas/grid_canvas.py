from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import numpy as np
from matnimation.artist.base_artist import BaseArtist
from matnimation.canvas.canvas import Canvas

class GridCanvas(Canvas):
    
    def __init__(
            self, 
            figsize : tuple, 
            dpi : int, 
            time_array: np.ndarray[float],
            nrows: int,
            ncols: int,
            spans: list[slice],
            axes_keys: list[str],
            axes_limits: list,          
            axes_labels: list, 
            width_ratios = None, 
            height_ratios = None,
            ):
        """Docstring goes here."""

        super().__init__(figsize, dpi, time_array)

        self.nrows = nrows
        self.ncols = ncols
        self.spans = spans                      # [[span_rows, span_cols],[],[]] span_rows, span_cols can be int or 2D list if spans multiple cols/rows 
        self.axes_keys = axes_keys              # must have same length as spans      
        self.axes_limits = axes_limits
        self.axes_labels = axes_labels
        self.width_ratios = width_ratios
        self.height_ratios = height_ratios

        self.fig = plt.figure(figsize = self.figsize, constrained_layout = True, animated = False)

        self.grid = plt.GridSpec(
            self.nrows, 
            self.ncols, 
            figure = self.fig, 
            height_ratios = self.height_ratios,
            width_ratios = self.width_ratios
            )
        
        self.axs_array = np.empty(len(self.spans), dtype = Axes)

        for i, span in enumerate(self.spans):
            span_row, span_col = span[0], span[1]

            if isinstance(span_row, list):
                span_row = slice(span_row[0], span_row[1] + 1)

            if isinstance(span_col, list):
                span_col = slice(span_col[0], span_col[1] + 1)

            ax = self.fig.add_subplot(self.grid[span_row, span_col])
            ax.set_animated(False)
            self.axs_array[i] = ax

        self.axs_dict = dict(zip(self.axes_keys, self.axs_array))

        self.set_layout(self.fig, self.axs_array, self.axes_limits, self.axes_labels)
        
        self.legend_handles_collection = {axis_key:set() for axis_key in self.axes_keys}

    def get_axis(self, axes_key: str):
        ax = self.axs_dict[axes_key]
        return ax

    def set_axis_properties(self, axes_key: str, **axis_styling):
        """Set styling properties of axis with axis_key, all kwargs of Matplotlib Axis artist can be passed here."""

        ax = self.get_axis(axes_key)
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

    

    
        