# https://matplotlib.org/3.2.1/gallery/images_contours_and_fields/image_demo.html

import sys

import matplotlib
import matplotlib.cbook as cbook
import matplotlib.cm as cm
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QListWidget,
                             QStackedWidget, QWidget)


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.list_widget = QListWidget()
        self.stacked_widget = QStackedWidget()

        lay = QHBoxLayout(self)
        lay.addWidget(self.list_widget)
        lay.addWidget(self.stacked_widget)

        for name, w in (
            ("bivariate normal distribution", self.canvas_1()),
            ("images of pictures", self.canvas_2()),
            ("Interpolating images 1", self.canvas_3()),
            ("Interpolating images 2", self.canvas_4()),
            ("Interpolating images 3", self.canvas_5()),
        ):
            self.list_widget.addItem(name)
            self.stacked_widget.addWidget(w)

        self.list_widget.selectionModel().currentChanged.connect(
            lambda index: self.stacked_widget.setCurrentIndex(index.row())
        )

        self.list_widget.setFixedWidth(200)

    def canvas_1(self):

        canvas = FigureCanvas(Figure(figsize=(8, 6)))

        delta = 0.025
        x = y = np.arange(-3.0, 3.0, delta)
        X, Y = np.meshgrid(x, y)
        Z1 = np.exp(-(X ** 2) - Y ** 2)
        Z2 = np.exp(-((X - 1) ** 2) - (Y - 1) ** 2)
        Z = (Z1 - Z2) * 2

        ax = canvas.figure.subplots()
        im = ax.imshow(
            Z,
            interpolation="bilinear",
            cmap=cm.RdYlGn,
            origin="lower",
            extent=[-3, 3, -3, 3],
            vmax=abs(Z).max(),
            vmin=-abs(Z).max(),
        )
        return canvas

    def canvas_2(self):

        canvas1 = FigureCanvas(Figure(figsize=(8, 6)))

        with cbook.get_sample_data("ada.png") as image_file:
            image = matplotlib.image.imread(image_file)

        ax = canvas1.figure.subplots()
        ax.imshow(image)
        ax.axis("off")  # clear x-axis and y-axis

        # And another image

        w, h = 512, 512

        with cbook.get_sample_data("ct.raw.gz") as datafile:
            s = datafile.read()
        A = np.frombuffer(s, np.uint16).astype(float).reshape((w, h))
        A /= A.max()

        canvas2 = FigureCanvas(Figure(figsize=(8, 6)))

        ax = canvas2.figure.subplots()
        extent = (0, 25, 0, 25)
        im = ax.imshow(A, cmap=cm.hot, origin="upper", extent=extent)

        markers = [(15.9, 14.5), (16.8, 15)]
        x, y = zip(*markers)
        ax.plot(x, y, "o")

        ax.set_title("CT density")

        w = QWidget()
        w.setContentsMargins(0, 0, 0, 0)
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(canvas1)
        lay.addWidget(canvas2)

        return w

    def canvas_3(self):
        A = np.random.rand(5, 5)
        canvas = FigureCanvas(Figure(figsize=(8, 6)))
        axs = canvas.figure.subplots(1, 3)
        for ax, interp in zip(axs, ["nearest", "bilinear", "bicubic"]):
            ax.imshow(A, interpolation=interp)
            ax.set_title(interp.capitalize())
            ax.grid(True)

        return canvas

    def canvas_4(self):

        canvas = FigureCanvas(Figure(figsize=(8, 6)))

        x = np.arange(120).reshape((10, 12))

        interp = "bilinear"
        axs = canvas.figure.subplots(nrows=2, sharex=True)
        axs[0].set_title("blue should be up")
        axs[0].imshow(x, origin="upper", interpolation=interp)

        axs[1].set_title("blue should be down")
        axs[1].imshow(x, origin="lower", interpolation=interp)

        return canvas

    def canvas_5(self):

        canvas = FigureCanvas(Figure(figsize=(8, 6)))

        delta = 0.025
        x = y = np.arange(-3.0, 3.0, delta)
        X, Y = np.meshgrid(x, y)
        Z1 = np.exp(-(X ** 2) - Y ** 2)
        Z2 = np.exp(-((X - 1) ** 2) - (Y - 1) ** 2)
        Z = (Z1 - Z2) * 2

        path = Path([[0, 1], [1, 0], [0, -1], [-1, 0], [0, 1]])
        patch = PathPatch(path, facecolor="none")

        ax = canvas.figure.subplots()
        ax.add_patch(patch)

        im = ax.imshow(
            Z,
            interpolation="bilinear",
            cmap=cm.gray,
            origin="lower",
            extent=[-3, 3, -3, 3],
            clip_path=patch,
            clip_on=True,
        )
        im.set_clip_path(patch)

        return canvas


def main():
    app = QApplication(sys.argv)

    w = Widget()
    w.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
