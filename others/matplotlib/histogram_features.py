# -*- coding: utf-8 -*-
# https://matplotlib.org/3.2.1/gallery/statistics/histogram_features.html

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

np.random.seed(19680801)

# example data
mu = 100  # mean of distribution
sigma = 15  # standard deviation of distribution
x = mu + sigma * np.random.randn(437)

num_bins = 50

ax = fig.subplots()

# the histogram of the data
n, bins, patches = ax.hist(x, num_bins, density=1)

# add a 'best fit' line
y = (1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * (1 / sigma * (bins - mu)) ** 2)
ax.plot(bins, y, "--")
ax.set_xlabel("Smarts")
ax.set_ylabel("Probability density")
ax.set_title(r"Histogram of IQ: $\mu=100$, $\sigma=15$")

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()

sys.exit(app.exec_())
