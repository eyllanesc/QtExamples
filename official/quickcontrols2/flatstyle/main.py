# -*- coding: utf-8 -*-
from Qt.QtCore import QCoreApplication, Qt, QUrl
from Qt.QtQml import QQmlApplicationEngine
from Qt.QtWidgets import QApplication

import resources_rc  # noqa: F401


def main():
    import sys

    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.addImportPath(":/imports")
    engine.load(QUrl("qrc:/flatstyle.qml"))

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
