from matplotlib.axes import Axes
from matplotlib.text import Text
from matnimation.artist.static.static_artist import StaticArtist


class StaticText(StaticArtist):

    def __init__(self, name: str, xy_center: tuple[float]):
        """
        StaticCircle

        Arguments:
        name      (float or int)  radius of circle
        xy_center   (tuple)         (x,y) coordinates of text location

        """

        super().__init__(name)
        self.xy_center = xy_center

        self.x, self.y = self.xy_center

        self.artist = Text(
            x = self.x,
            y = self.y,
            text = self.name
        )

        
