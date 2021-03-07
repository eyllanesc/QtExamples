# -*- coding: utf-8 -*-
from Qt.QtCore import Qt, QUrl
from Qt.QtGui import QFontDatabase, QGuiApplication
from Qt.QtQml import QQmlApplicationEngine

import resources_rc  # noqa: F401


def main():
    import sys

    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QGuiApplication(sys.argv)

    QFontDatabase.addApplicationFont(":/fonts/fontello.ttf")

    engine = QQmlApplicationEngine()
    engine.load(QUrl("qrc:/swipetoremove.qml"))
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
