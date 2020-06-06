from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QAction, QMainWindow, QWidget

from lightmaps import LightMaps


class MapZoom(QMainWindow):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.map = LightMaps()

        self.setCentralWidget(self.map)
        self.map.setFocus()

        osloAction = QAction(self.tr("&Oslo"), self)
        berlinAction = QAction(self.tr("&Berlin"), self)
        jakartaAction = QAction(self.tr("&Jakarta"), self)
        nightModeAction = QAction(self.tr("Night Mode"), self)
        nightModeAction.setCheckable(True)
        nightModeAction.setChecked(False)
        osmAction = QAction(self.tr("About OpenStreetMap"), self)
        osloAction.triggered.connect(self.chooseOslo)
        berlinAction.triggered.connect(self.chooseBerlin)
        jakartaAction.triggered.connect(self.chooseJakarta)
        nightModeAction.triggered.connect(self.map.toggleNightMode)
        osmAction.triggered.connect(self.aboutOsm)

        menu = self.menuBar().addMenu(self.tr("&Options"))
        menu.addAction(osloAction)
        menu.addAction(berlinAction)
        menu.addAction(jakartaAction)
        menu.addSeparator()
        menu.addAction(nightModeAction)
        menu.addAction(osmAction)

        self.setWindowTitle(self.tr("Light Maps"))

    @pyqtSlot()
    def chooseOslo(self):
        self.map.setCenter(59.9138204, 10.7387413)

    @pyqtSlot()
    def chooseBerlin(self):
        self.map.setCenter(52.52958999943302, 13.383053541183472)

    @pyqtSlot()
    def chooseJakarta(self):
        self.map.setCenter(-6.211544, 106.845172)

    @pyqtSlot()
    def aboutOsm(self):
        QDesktopServices.openUrl(QUrl("http://www.openstreetmap.org"))
