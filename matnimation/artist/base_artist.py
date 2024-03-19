from abc import ABC, abstractmethod
from matplotlib.artist import Artist as Artist
from matplotlib.axes import Axes

class BaseArtist(ABC): 
    """Object (line, circle, arrow etc) to be placed on a specific axis of a defined canvas."""

    def __init__(self, name: str):
        # name of object
        self.name = name

        # this is the matplotlib Artist object to be defined in all subclasses. 
        self.artist: Artist = None

        # this is the Legend handle to be defined in all subclasses (could be Proxy artists)
        self.legend_handle: Artist = None
        

    def set_styling_properties(self, **styling):
        """Set styling properties, all kwargs of matplotlib Artist can be passed here."""

        self.artist.set(**styling)

    # add artist to axes #WARNING: For some artists (like quiver vector plots), this method will be overwritten
    def add_to_axes(self, axes: Axes):
        axes.add_artist(self.artist)

    # get handle for legend 
    def get_legend_handle(self):
        return self.legend_handle
    
    # this is an abstract method, since it MUST be implemented by the subclasses, but how this is done depends on the kind of Artist (static or animated).
    # if animated, it still depends on which type of artist is updated. 
    @abstractmethod
    def update_timestep(self, time_index: int):
        pass