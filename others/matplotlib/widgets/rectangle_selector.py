# https://matplotlib.org/examples/widgets/rectangle_selector.html

import sys

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

fig = Figure(figsize=(8, 6))
canvas = FigureCanvas(fig)
canvas.resize(640, 480)
canvas.show()


def line_select_callback(eclick, erelease):
    "eclick and erelease are the press and release events"
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    print("({:3.2f}, {:3.2f}) --> ({:3.2f}, {:3.2f})".format(x1, y1, x2, y2))
    print(" The button you used were: {} {}".format(eclick.button, erelease.button))


def toggle_selector(event):
    print(" Key pressed.")
    if event.key in ["Q", "q"] and toggle_selector.RS.active:
        print(" RectangleSelector deactivated.")
        toggle_selector.RS.set_active(False)
    if event.key in ["A", "a"] and not toggle_selector.RS.active:
        print(" RectangleSelector activated.")
        toggle_selector.RS.set_active(True)


current_ax = fig.subplots()  # make a new plotting range
N = 100000  # If N is large one can see
x = np.linspace(0.0, 10.0, N)  # improvement by use blitting!

current_ax.plot(x, +np.sin(0.2 * np.pi * x), lw=3.5, c="b", alpha=0.7)  # plot something
current_ax.plot(x, +np.cos(0.2 * np.pi * x), lw=3.5, c="r", alpha=0.5)
current_ax.plot(x, -np.sin(0.2 * np.pi * x), lw=3.5, c="g", alpha=0.3)

print("\n      click  -->  release")

# drawtype is 'box' or 'line' or 'none'
toggle_selector.RS = RectangleSelector(
    current_ax,
    line_select_callback,
    drawtype="box",
    useblit=True,
    button=[1, 3],  # don't use middle button
    minspanx=5,
    minspany=5,
    spancoords="pixels",
    interactive=True,
)
canvas.mpl_connect("key_press_event", toggle_selector)

sys.exit(app.exec_())
