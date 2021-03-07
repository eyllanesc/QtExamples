# -*- coding: utf-8 -*-
# https://matplotlib.org/3.2.1/gallery/scales/log_demo.html

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
t = np.arange(0.01, 20.0, 0.01)

# Create figure
((ax1, ax2), (ax3, ax4)) = fig.subplots(2, 2)

# log y axis
ax1.semilogy(t, np.exp(-t / 5.0))
ax1.set(title="semilogy")
ax1.grid()

# log x axis
ax2.semilogx(t, np.sin(2 * np.pi * t))
ax2.set(title="semilogx")
ax2.grid()

# log x and y axis
ax3.loglog(t, 20 * np.exp(-t / 10.0), basex=2)
ax3.set(title="loglog base 2 on x")
ax3.grid()

# With errorbars: clip non-positive values
# Use new data for plotting
x = 10.0 ** np.linspace(0.0, 2.0, 20)
y = x ** 2.0

ax4.set_xscale("log", nonposx="clip")
ax4.set_yscale("log", nonposy="clip")
ax4.set(title="Errorbars go negative")
ax4.errorbar(x, y, xerr=0.1 * x, yerr=5.0 + 0.75 * y)
# ylim must be set after errorbar to allow errorbar to autoscale limits
ax4.set_ylim(bottom=0.1)

fig.tight_layout()

sys.exit(app.exec_())
