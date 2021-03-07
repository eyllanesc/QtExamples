# -*- coding: utf-8 -*-
from Qt.QtCore import QSettings, Qt, QUrl
from Qt.QtGui import QGuiApplication, QIcon
from Qt.QtQml import QQmlApplicationEngine

from qmissings.QtQuickControls2 import QQuickStyle

import resources_rc  # noqa: F401


def main():
    import sys

    QGuiApplication.setApplicationName("Gallery")
    QGuiApplication.setOrganizationName("QtProject")
    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QGuiApplication(sys.argv)

    QIcon.setThemeName("gallery")

    settings = QSettings()

    style = QQuickStyle.name()
    if style:
        settings.setValue("style", style)
    else:
        QQuickStyle.setStyle(settings.value("style"))

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty(
        "availableStyles", QQuickStyle.availableStyles()
    )
    engine.load(QUrl("qrc:/gallery.qml"))
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
