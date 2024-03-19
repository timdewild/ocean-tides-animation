from typing import Any
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import numpy as np
from matnimation.artist.base_artist import BaseArtist

from matnimation.artist.animated.animated_artist import AnimatedArtist


class Canvas:
    def __init__(self, figsize : tuple, dpi : int, time_array: np.ndarray[float]):
        """
        Initialize Canvas.

        Arguments:
        figsize             (2D tuple)      figure size (width, height) in inches
        dpi                 (float)         dots per inch, resolution of canvas, set to 200 by default    
        """

        self.figsize = figsize
        self.dpi = dpi
        self.time_array = time_array


        # define a set to contain all artists living on the canvas (set so that every instance of BaseArtist can only be added once)
        self.artists: set[BaseArtist] = set(())
        self.fig: Figure = None
        self.axs_array = np.ndarray[Axes]
    

    def update_frame(self, time_index: int):
        for artist in self.artists:
            artist.update_timestep(time_index)  

    # this method is protected (using underscore_), as it should be accesible in Canvas class and its subclasses, but not outside
    def _add_artist(self, artist: BaseArtist):
        self.artists.add(artist)
    
    def set_figure_properties(self, **figure_styling):
        """Set styling properties of canvas, all kwargs of Matplotlib Figure artist can be passed here."""
        
        self.fig.set(**figure_styling)

    def get_figure(self) -> Figure:
        return self.fig
    
    def save_canvas(self, filename: str):
        fig = self.get_figure()
        fig.savefig(filename, dpi=self.dpi)

    def set_layout(self, fig: Figure, axs_array: np.ndarray[Axes], axes_limits: list[float], axes_labels: list[str]):
        """
        fig and axs_array are created in the Subclasses of Canvans (SingleCanvas, MultiCanvas, CustomCanvas)
        axis_limits must be 2D list of form [[xmin, xmax, ymin, ymax],[xmin, xmax, ymin, ymax],...]
        axis_labels must be 2D list of form [[xlabel, ylabel],[xlabel, ylabel],...] where the first sublist corresponds to the first axis
        
        In those lists, the first sublist corresponds to the first axis (top-left). 
        The order of the axes is left-to-right and top-to-bottom of their position in the total layout.
        """
       
        fig.set_dpi(self.dpi)

        ax: Axes
        for i, ax in enumerate(axs_array.flatten()):
            ax.axis(axes_limits[i])
            ax.set_xlabel(axes_labels[i][0])
            ax.set_ylabel(axes_labels[i][1])
            ax.grid(True, color=u'white', lw=1.5, zorder=0)
            ax.set_facecolor('#EEEEEE')  

    def get_axs_array(self):
        return self.axs_array

    def add_legend(self, axes: Axes, legend_handles: set, **legend_styling):
        """
        Given an Axes object 'axes' and a set of 'legend_handels, add legend to 'axes'.
        
        **legend_styling contains all the 'other parameters' of the Axes.legend() for styling.
        """
        axes.legend(handles = legend_handles, **legend_styling)
