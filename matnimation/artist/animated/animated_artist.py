from abc import ABC
from matnimation.artist.base_artist import BaseArtist


class AnimatedArtist(BaseArtist, ABC):
    """Animated Artist (line, circle, arrow etc) to be placed on a specific axis of a defined canvas."""

    def __init__(self, name: str, vis_interval: list[int] = None):
        super().__init__(name)

        # set z order
        self.zorder = 3
        
        
        # list with time_indices at which visiblity must turned ON and OFF, if vis_interval = [1,10], vis will be turned ON at time index 1 and turned OFF at time_index 10
        # if vis_interval = [1,10, 20, 30], visiblity will turned on at 1 and 20 and off at 10 and 30
        self.vis_interval = vis_interval  

    def update_visibility(self, time_index: int):
        if self.vis_interval:
            ti_appear = self.vis_interval[0]
            ti_dissappear = self.vis_interval[1]

            self.artist.set_visible(False)

            if time_index in range(ti_appear, ti_dissappear + 1):
                self.artist.set_visible(True)

        




