# -*- coding: utf-8 -*-
# https://matplotlib.org/3.2.1/gallery/images_contours_and_fields/plot_streamplot.html

import sys

import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

fig = Figure(figsize=(7, 9))
canvas = FigureCanvas(fig)
canvas.resize(640, 480)
canvas.show()

w = 3
Y, X = np.mgrid[-w:w:100j, -w:w:100j]
U = -1 - X ** 2 + Y
V = 1 + X - Y ** 2
speed = np.sqrt(U ** 2 + V ** 2)

gs = gridspec.GridSpec(nrows=3, ncols=2, height_ratios=[1, 1, 2])

#  Varying density along a streamline
ax0 = fig.add_subplot(gs[0, 0])
ax0.streamplot(X, Y, U, V, density=[0.5, 1])
ax0.set_title("Varying Density")

# Varying color along a streamline
ax1 = fig.add_subplot(gs[0, 1])
strm = ax1.streamplot(X, Y, U, V, color=U, linewidth=2, cmap="autumn")
fig.colorbar(strm.lines)
ax1.set_title("Varying Color")

#  Varying line width along a streamline
ax2 = fig.add_subplot(gs[1, 0])
lw = 5 * speed / speed.max()
ax2.streamplot(X, Y, U, V, density=0.6, color="k", linewidth=lw)
ax2.set_title("Varying Line Width")

# Controlling the starting points of the streamlines
seed_points = np.array([[-2, -1, 0, 1, 2, -1], [-2, -1, 0, 1, 2, 2]])

ax3 = fig.add_subplot(gs[1, 1])
strm = ax3.streamplot(
    X, Y, U, V, color=U, linewidth=2, cmap="autumn", start_points=seed_points.T
)
fig.colorbar(strm.lines)
ax3.set_title("Controlling Starting Points")

# Displaying the starting points with blue symbols.
ax3.plot(seed_points[0], seed_points[1], "bo")
ax3.set(xlim=(-w, w), ylim=(-w, w))

# Create a mask
mask = np.zeros(U.shape, dtype=bool)
mask[40:60, 40:60] = True
U[:20, :20] = np.nan
U = np.ma.array(U, mask=mask)

ax4 = fig.add_subplot(gs[2:, :])
ax4.streamplot(X, Y, U, V, color="r")
ax4.set_title("Streamplot with Masking")

ax4.imshow(
    ~mask,
    extent=(-w, w, -w, w),
    alpha=0.5,
    interpolation="nearest",
    cmap="gray",
    aspect="auto",
)
ax4.set_aspect("equal")

fig.tight_layout()

sys.exit(app.exec_())
