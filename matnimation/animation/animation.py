from matplotlib import animation
import numpy as np

from matnimation.canvas.canvas import Canvas

class Animation:
    def __init__(self, canvas : Canvas, interval : int = 30):
        self.canvas = canvas
        self.interval = interval

        self.fig = self.canvas.get_figure()

    def animate(self, time_index: int):
        self.canvas.update_frame(time_index)

    def render(self, filename):
        anim = animation.FuncAnimation(self.fig, self.animate, frames = len(self.canvas.time_array), interval = self.interval)
        anim.save(filename = filename)