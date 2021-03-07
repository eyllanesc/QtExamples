# -*- coding: utf-8 -*-
import os.path
import sys


from PySide2.QtCore import QCoreApplication, Qt, QUrl
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

from video import register_types


register_types()
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def main():
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()

    filename = os.path.join(CURRENT_DIR, "qml", "main.qml")
    url = QUrl.fromLocalFile(filename)

    def handle_object_created(obj, objUrl):
        if not obj and url == objUrl:
            QCoreApplication.exit(-1)

    engine.objectCreated.connect(handle_object_created, Qt.QueuedConnection)

    engine.load(url)

    ret = app.exec_()
    sys.exit(ret)


if __name__ == "__main__":
    main()
