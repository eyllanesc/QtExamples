# -*- coding: utf-8 -*-
# https://matplotlib.org/examples/widgets/buttons.html

import sys

from PyQt5.QtWidgets import QApplication

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import Button

freqs = np.arange(2, 20, 3)

app = QApplication(sys.argv)

figure = Figure()
canvas = FigureCanvas(figure)
canvas.resize(640, 480)
canvas.show()

ax = figure.subplots()
figure.subplots_adjust(bottom=0.2)
t = np.arange(0.0, 1.0, 0.001)
s = np.sin(2 * np.pi * freqs[0] * t)
(l,) = ax.plot(t, s, lw=2)


class Index(object):
    ind = 0

    def next(self, event):
        self.ind += 1
        i = self.ind % len(freqs)
        ydata = np.sin(2 * np.pi * freqs[i] * t)
        l.set_ydata(ydata)
        canvas.draw()

    def prev(self, event):
        self.ind -= 1
        i = self.ind % len(freqs)
        ydata = np.sin(2 * np.pi * freqs[i] * t)
        l.set_ydata(ydata)
        canvas.draw()


callback = Index()
axprev = figure.add_axes([0.7, 0.05, 0.1, 0.075])
axnext = figure.add_axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, "Next")
bnext.on_clicked(callback.next)
bprev = Button(axprev, "Previous")
bprev.on_clicked(callback.prev)


sys.exit(app.exec_())
