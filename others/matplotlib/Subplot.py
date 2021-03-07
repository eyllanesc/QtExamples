# -*- coding: utf-8 -*-
# https://matplotlib.org/3.2.1/tutorials/introductory/sample_plots.html#subplot-example

import sys

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

fig = Figure(figsize=(5, 5))
canvas = FigureCanvas(fig)
canvas.resize(640, 480)
canvas.show()

np.random.seed(19680801)
data = np.random.randn(2, 100)

axs = fig.subplots(2, 2)
axs[0, 0].hist(data[0])
axs[1, 0].scatter(data[0], data[1])
axs[0, 1].plot(data[0], data[1])
axs[1, 1].hist2d(data[0], data[1])

sys.exit(app.exec_())
