# https://matplotlib.org/examples/widgets/radio_buttons.html

import sys

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import RadioButtons
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

fig = Figure(figsize=(8, 6))
canvas = FigureCanvas(fig)
canvas.resize(640, 480)
canvas.show()


t = np.arange(0.0, 2.0, 0.01)
s0 = np.sin(2 * np.pi * t)
s1 = np.sin(4 * np.pi * t)
s2 = np.sin(8 * np.pi * t)

ax = fig.subplots()
(l,) = ax.plot(t, s0, lw=2, color="red")
fig.subplots_adjust(left=0.3)

axcolor = "lightgoldenrodyellow"
rax = fig.add_axes([0.05, 0.7, 0.15, 0.15], facecolor=axcolor)
radio = RadioButtons(rax, ("2 Hz", "4 Hz", "8 Hz"))


def hzfunc(label):
    hzdict = {"2 Hz": s0, "4 Hz": s1, "8 Hz": s2}
    ydata = hzdict[label]
    l.set_ydata(ydata)
    canvas.draw()


radio.on_clicked(hzfunc)

rax = fig.add_axes([0.05, 0.4, 0.15, 0.15], facecolor=axcolor)
radio2 = RadioButtons(rax, ("red", "blue", "green"))


def colorfunc(label):
    l.set_color(label)
    canvas.draw()


radio2.on_clicked(colorfunc)

rax = fig.add_axes([0.05, 0.1, 0.15, 0.15], facecolor=axcolor)
radio3 = RadioButtons(rax, ("-", "--", "-.", "steps", ":"))


def stylefunc(label):
    l.set_linestyle(label)
    canvas.draw()


radio3.on_clicked(stylefunc)

sys.exit(app.exec_())
