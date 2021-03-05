# https://matplotlib.org/examples/widgets/multicursor.html

import sys

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import MultiCursor
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

fig = Figure(figsize=(8, 6))
canvas = FigureCanvas(fig)
canvas.resize(640, 480)
canvas.show()

t = np.arange(0.0, 2.0, 0.01)
s1 = np.sin(2 * np.pi * t)
s2 = np.sin(4 * np.pi * t)

ax1 = fig.add_subplot(211)
ax1.plot(t, s1)


ax2 = fig.add_subplot(212, sharex=ax1)
ax2.plot(t, s2)

multi = MultiCursor(fig.canvas, (ax1, ax2), color="r", lw=1)

sys.exit(app.exec_())
