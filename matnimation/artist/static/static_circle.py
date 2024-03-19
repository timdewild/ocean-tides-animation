from matplotlib import patches
from matplotlib.axes import Axes
from matnimation.artist.static.static_artist import StaticArtist


class StaticCircle(StaticArtist):

    def __init__(self, name: str, radius: float, xy_center: tuple[float]):
        """
        StaticCircle

        Arguments:
        radius      (float or int)  radius of circle
        xy_center   (tuple)         (x,y) coordinates of the center

        """

        super().__init__(name)
        self.radius = radius
        self.xy_center = xy_center

        self.artist = patches.Circle(xy_center, radius = self.radius, zorder = self.zorder, label = self.name)
        self.legend_handle = self.artist

    