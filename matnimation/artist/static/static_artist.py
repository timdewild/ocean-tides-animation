from matnimation.artist.base_artist import BaseArtist

class StaticArtist(BaseArtist):
    """Static Artist (line, circle, arrow etc) to be placed on a specific axis of a defined canvas."""

    def __init__(self, name: str):
        super().__init__(name)

        # set z order
        self.zorder = 2

    def update_timestep(self, time_index: int):
        pass