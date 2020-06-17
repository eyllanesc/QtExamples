# https://matplotlib.org/examples/widgets/check_buttons.html

import sys

from PyQt5.QtWidgets import QApplication

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import CheckButtons

t = np.arange(0.0, 2.0, 0.01)
s0 = np.sin(2 * np.pi * t)
s1 = np.sin(4 * np.pi * t)
s2 = np.sin(6 * np.pi * t)

app = QApplication(sys.argv)

figure = Figure()
canvas = FigureCanvas(figure)
canvas.resize(640, 480)
canvas.show()

ax = figure.subplots()
(l0,) = ax.plot(t, s0, visible=False, lw=2)
(l1,) = ax.plot(t, s1, lw=2)
(l2,) = ax.plot(t, s2, lw=2)
figure.subplots_adjust(left=0.2)

rax = figure.add_axes([0.05, 0.4, 0.1, 0.15])
check = CheckButtons(rax, ("2 Hz", "4 Hz", "6 Hz"), (False, True, True))


def func(label):
    if label == "2 Hz":
        l0.set_visible(not l0.get_visible())
    elif label == "4 Hz":
        l1.set_visible(not l1.get_visible())
    elif label == "6 Hz":
        l2.set_visible(not l2.get_visible())
    canvas.draw()


check.on_clicked(func)


sys.exit(app.exec_())
