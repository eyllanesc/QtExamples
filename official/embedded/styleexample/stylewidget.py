from PyQt5.QtCore import pyqtSlot, QFile, QIODevice
from PyQt5.QtWidgets import qApp, QFrame, QWidget

from stylewidget_ui import Ui_StyleWidget
import styleexample_rc  # noqa: F401


class StyleWidget(QFrame):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.m_ui = Ui_StyleWidget()
        self.m_ui.setupUi(self)

    @pyqtSlot()
    def on_close_clicked(self):
        self.close()

    @pyqtSlot()
    def on_blueStyle_clicked(self):
        styleSheet = QFile(":/files/blue.qss")

        if not styleSheet.open(QIODevice.ReadOnly):
            print("Unable to open :/files/blue.qss")
            return

        qApp.setStyleSheet(styleSheet.readAll().data().decode())

    @pyqtSlot()
    def on_khakiStyle_clicked(self):
        styleSheet = QFile(":/files/khaki.qss")

        if not styleSheet.open(QIODevice.ReadOnly):
            print("Unable to open :/files/khaki.qss")
            return

        qApp.setStyleSheet(styleSheet.readAll().data().decode())

    @pyqtSlot()
    def on_noStyle_clicked(self):
        styleSheet = QFile(":/files/nostyle.qss")

        if not styleSheet.open(QIODevice.ReadOnly):
            print("Unable to open :/files/nostyle.qss")
            return

        qApp.setStyleSheet(styleSheet.readAll().data().decode())

    @pyqtSlot()
    def on_transparentStyle_clicked(self):
        styleSheet = QFile(":/files/transparent.qss")

        if not styleSheet.open(QIODevice.ReadOnly):
            print("Unable to open :/files/transparent.qss")
            return

        qApp.setStyleSheet(styleSheet.readAll().data().decode())
