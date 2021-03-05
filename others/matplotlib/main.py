import sys
import uuid

from PyQt5 import QtCore, QtWidgets

import animatplot as amp
import cartopy.crs as ccrs
import geopandas as gpd
import geoplot as gplt
import geoplot.crs as gcrs
import numpy as np
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap

pd.set_option("max_columns", 6)  # Unclutter display.


class MatplotlibApplication:
    def __init__(self):
        self._callbacks = dict()

    @property
    def callbacks(self):
        return self._callbacks

    def register(self, *, title):
        def decorator(f):
            self._callbacks[uuid.uuid4().hex] = (title, f)
            return f

        return decorator


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app, parent=None):
        super().__init__(parent)

        self.view = QtWidgets.QListWidget()

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.addToolBar(QtCore.Qt.TopToolBarArea, NavigationToolbar(self.canvas, self))

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        lay = QtWidgets.QGridLayout(central_widget)
        lay.addWidget(QtWidgets.QLabel(self.tr("<b>Select Example:</b>")))
        lay.addWidget(self.view, 1, 0)
        lay.addWidget(self.canvas, 1, 1)

        lay.setColumnStretch(0, 0)
        lay.setColumnStretch(1, 1)

        self.resize(640, 480)

        for _, (name, callback) in app.callbacks.items():
            it = QtWidgets.QListWidgetItem(name)
            it.setData(QtCore.Qt.UserRole, callback)
            self.view.addItem(it)

        self.view.currentRowChanged.connect(self.on_currentRowChanged)
        self.view.setCurrentRow(0)

    @QtCore.pyqtSlot(int)
    def on_currentRowChanged(self, row):
        self.canvas.figure.clear()
        item = self.view.item(row)
        callback = item.data(QtCore.Qt.UserRole)
        callback(self.canvas)
        self.canvas.draw()


matplotlib_app = MatplotlibApplication()


@matplotlib_app.register(title="Basemap")
def basemap(canvas):
    # https://matplotlib.org/basemap/users/examples.html
    ax = canvas.figure.subplots()
    # set up orthographic map projection with
    # perspective of satellite looking down at 50N, 100W.
    # use low resolution coastlines.
    map = Basemap(projection="ortho", lat_0=45, lon_0=-100, resolution="l", ax=ax)
    # draw coastlines, country boundaries, fill continents.
    map.drawcoastlines(linewidth=0.25)
    map.drawcountries(linewidth=0.25)
    map.fillcontinents(color="coral", lake_color="aqua")
    # draw the edge of the map projection region (the projection limb)
    map.drawmapboundary(fill_color="aqua")
    # draw lat/lon grid lines every 30 degrees.
    map.drawmeridians(np.arange(0, 360, 30))
    map.drawparallels(np.arange(-90, 90, 30))
    # make up some data on a regular lat/lon grid.
    nlats = 73
    nlons = 145
    delta = 2.0 * np.pi / (nlons - 1)
    lats = 0.5 * np.pi - delta * np.indices((nlats, nlons))[0, :, :]
    lons = delta * np.indices((nlats, nlons))[1, :, :]
    wave = 0.75 * (np.sin(2.0 * lats) ** 8 * np.cos(4.0 * lons))
    mean = 0.5 * np.cos(2.0 * lats) * ((np.sin(2.0 * lats)) ** 2 + 2.0)
    # compute native map projection coordinates of lat/lon grid.
    x, y = map(lons * 180.0 / np.pi, lats * 180.0 / np.pi)
    # contour data over the map.
    cs = map.contour(x, y, wave + mean, 15, linewidths=1.5)  # noqa: F841
    ax.set_title("contour lines over filled continent background")


@matplotlib_app.register(title="cartopy")
def cartopy(canvas):
    ax = canvas.figure.add_subplot(1, 1, 1, projection=ccrs.Robinson())
    ax.set_global()

    ax.stock_img()
    ax.coastlines()

    ax.plot(-0.08, 51.53, "o", transform=ccrs.PlateCarree())
    ax.plot([-0.08, 132], [51.53, 43.17], transform=ccrs.PlateCarree())
    ax.plot([-0.08, 132], [51.53, 43.17], transform=ccrs.Geodetic())


@matplotlib_app.register(title="Geoplot")
def geoplot(canvas):
    obesity = pd.read_csv(gplt.datasets.get_path("obesity_by_state"), sep="\t")
    contiguous_usa = gpd.read_file(gplt.datasets.get_path("contiguous_usa"))
    result = contiguous_usa.set_index("state").join(obesity.set_index("State"))
    # https://stackoverflow.com/a/51621986/6622587
    ax = canvas.figure.subplots(subplot_kw={"projection": gcrs.AlbersEqualArea()})
    gplt.cartogram(result, scale="Percent", projection=gcrs.AlbersEqualArea(), ax=ax)


anim = None


@matplotlib_app.register(title="animatplot")
def animatplot(canvas):

    global anim

    ax = canvas.figure.subplots()

    x = np.linspace(0, 1, 50)
    t = np.linspace(0, 1, 20)

    X, T = np.meshgrid(x, t)
    Y = np.sin(2 * np.pi * (X + T))

    block = amp.blocks.Line(X, Y, ax=ax)

    canvas.figure.subplots_adjust(
        top=0.8
    )  # squish the plot to make space for the controls
    slider_ax = canvas.figure.add_axes([0.18, 0.89, 0.5, 0.03])  # the rect of the axis
    button_ax = canvas.figure.add_axes([0.78, 0.87, 0.1, 0.07])  # x, y, width, height

    anim = amp.Animation([block], fig=canvas.figure)

    anim.toggle(ax=button_ax)
    anim.timeline_slider(text="TIME", ax=slider_ax, color="red", valfmt="%1.0f")


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(matplotlib_app)
    w.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
