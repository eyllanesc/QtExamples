# -*- coding: utf-8 -*-
# https://matplotlib.org/3.2.1/gallery/lines_bars_and_markers/fill.html

import sys

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication


def koch_snowflake(order, scale=10):
    """
    Return two lists x, y of point coordinates of the Koch snowflake.

    Arguments
    ---------
    order : int
        The recursion depth.
    scale : float
        The extent of the snowflake (edge length of the base triangle).
    """

    def _koch_snowflake_complex(order):
        if order == 0:
            # initial triangle
            angles = np.array([0, 120, 240]) + 90
            return scale / np.sqrt(3) * np.exp(np.deg2rad(angles) * 1j)
        else:
            ZR = 0.5 - 0.5j * np.sqrt(3) / 3

            p1 = _koch_snowflake_complex(order - 1)  # start points
            p2 = np.roll(p1, shift=-1)  # end points
            dp = p2 - p1  # connection vectors

            new_points = np.empty(len(p1) * 4, dtype=np.complex128)
            new_points[::4] = p1
            new_points[1::4] = p1 + dp / 3
            new_points[2::4] = p1 + dp * ZR
            new_points[3::4] = p1 + dp / 3 * 2
            return new_points

    points = _koch_snowflake_complex(order)
    x, y = points.real, points.imag
    return x, y


app = QApplication(sys.argv)

canvas1 = FigureCanvas(Figure(figsize=(8, 8)))
canvas1.resize(640, 480)
canvas1.show()

x, y = koch_snowflake(order=5)

ax = canvas1.figure.subplots()
ax.axis("equal")
ax.fill(x, y)

canvas2 = FigureCanvas(Figure(figsize=(8, 8)))
canvas2.resize(640, 480)
canvas2.show()

x, y = koch_snowflake(order=2)

(ax1, ax2, ax3) = canvas2.figure.subplots(1, 3, subplot_kw={"aspect": "equal"})
ax1.fill(x, y)
ax2.fill(x, y, facecolor="lightsalmon", edgecolor="orangered", linewidth=3)
ax3.fill(x, y, facecolor="none", edgecolor="purple", linewidth=3)

sys.exit(app.exec_())
