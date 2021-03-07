# -*- coding: utf-8 -*-
from Qt.QtCore import QFile, QIODevice, Slot
from Qt.QtWidgets import QApplication, QFrame, QWidget

import styleexample_rc  # noqa: F401
from stylewidget_ui import Ui_StyleWidget


class StyleWidget(QFrame):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.m_ui = Ui_StyleWidget()
        self.m_ui.setupUi(self)

    @Slot()
    def on_close_clicked(self):
        self.close()

    @Slot()
    def on_blueStyle_clicked(self):
        styleSheet = QFile(":/files/blue.qss")

        if not styleSheet.open(QIODevice.ReadOnly):
            print("Unable to open :/files/blue.qss")
            return

        QApplication.instance().setStyleSheet(styleSheet.readAll().data().decode())

    @Slot()
    def on_khakiStyle_clicked(self):
        styleSheet = QFile(":/files/khaki.qss")

        if not styleSheet.open(QIODevice.ReadOnly):
            print("Unable to open :/files/khaki.qss")
            return

        QApplication.instance().setStyleSheet(styleSheet.readAll().data().decode())

    @Slot()
    def on_noStyle_clicked(self):
        styleSheet = QFile(":/files/nostyle.qss")

        if not styleSheet.open(QIODevice.ReadOnly):
            print("Unable to open :/files/nostyle.qss")
            return

        QApplication.instance().setStyleSheet(styleSheet.readAll().data().decode())

    @Slot()
    def on_transparentStyle_clicked(self):
        styleSheet = QFile(":/files/transparent.qss")

        if not styleSheet.open(QIODevice.ReadOnly):
            print("Unable to open :/files/transparent.qss")
            return

        QApplication.instance().setStyleSheet(styleSheet.readAll().data().decode())
