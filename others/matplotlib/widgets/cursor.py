# https://matplotlib.org/examples/widgets/cursor.html

import sys

from PyQt5.QtWidgets import QApplication

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor

app = QApplication(sys.argv)

figure = Figure(figsize=(8, 6))
canvas = FigureCanvas(figure)
canvas.resize(640, 480)
canvas.show()

ax = figure.add_subplot(111, facecolor="#FFFFCC")

x, y = 4 * (np.random.rand(2, 100) - 0.5)
ax.plot(x, y, "o")
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)

cursor = Cursor(ax, useblit=True, color="red", linewidth=2)

sys.exit(app.exec_())
