# -*- coding: utf-8 -*-
# https://matplotlib.org/3.2.1/gallery/lines_bars_and_markers/simple_plot.html

import sys

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

fig = Figure(figsize=(8, 6))
canvas = FigureCanvas(fig)
canvas.resize(640, 480)
canvas.show()


# Data for plotting
t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2 * np.pi * t)

ax = fig.subplots()
ax.plot(t, s)

ax.set(
    xlabel="time (s)", ylabel="voltage (mV)", title="About as simple as it gets, folks"
)
ax.grid()

fig.savefig("test.png")

sys.exit(app.exec_())
