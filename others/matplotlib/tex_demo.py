# -*- coding: utf-8 -*-
# https://matplotlib.org/3.2.1/gallery/text_labels_and_annotations/tex_demo.html

import sys

import matplotlib
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication

matplotlib.rcParams["text.usetex"] = True

app = QApplication(sys.argv)

fig = Figure(figsize=(6, 4), tight_layout=True)
canvas = FigureCanvas(fig)
canvas.resize(640, 480)
canvas.show()

t = np.linspace(0.0, 1.0, 100)
s = np.cos(4 * np.pi * t) + 2

ax = fig.subplots()
ax.plot(t, s)

ax.set_xlabel(r"\textbf{time (s)}")
ax.set_ylabel("\\textit{Velocity (\N{DEGREE SIGN}/sec)}", fontsize=16)
ax.set_title(
    r"\TeX\ is Number $\displaystyle\sum_{n=1}^\infty" r"\frac{-e^{i\pi}}{2^n}$!",
    fontsize=16,
    color="r",
)

sys.exit(app.exec_())
