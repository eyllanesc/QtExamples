# -*- coding: utf-8 -*-
# https://matplotlib.org/3.2.1/gallery/subplots_axes_and_figures/subplot.html

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


x1 = np.linspace(0.0, 5.0)
x2 = np.linspace(0.0, 2.0)

y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
y2 = np.cos(2 * np.pi * x2)

ax1 = fig.add_subplot(2, 1, 1)
ax1.plot(x1, y1, "o-")
ax1.set_title("A tale of 2 subplots")
ax1.set_ylabel("Damped oscillation")

ax2 = fig.add_subplot(2, 1, 2)
ax2.plot(x2, y2, ".-")
ax2.set_xlabel("time (s)")
ax2.set_ylabel("Undamped")

sys.exit(app.exec_())
