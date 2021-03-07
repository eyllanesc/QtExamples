# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMainWindow, QTextEdit

from logfilepositionsource import LogFilePositionSource


class ClientApplication(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        source = LogFilePositionSource(self)
        source.positionUpdated.connect(self.positionUpdated)
        source.startUpdates()

    def positionUpdated(self, info):
        self.textEdit.append(
            "Position updated: Date/time = {}, Coordinate = {}".format(
                info.timestamp().toString(), info.coordinate().toString()
            )
        )
