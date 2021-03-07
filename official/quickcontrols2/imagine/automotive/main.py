# -*- coding: utf-8 -*-
from Qt.QtCore import Qt, QUrl
from Qt.QtGui import QGuiApplication, QIcon
from Qt.QtQml import QQmlApplicationEngine

import icons_rc  # noqa: F401
import imagine_assets_rc  # noqa: F401
import qml_rc  # noqa: F401
import resources_rc  # noqa: F401


def main():
    import sys

    QGuiApplication.setApplicationName("Automotive")
    QGuiApplication.setOrganizationName("QtProject")
    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QGuiApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QGuiApplication(sys.argv)

    QIcon.setThemeName("automotive")

    engine = QQmlApplicationEngine()
    engine.load(QUrl("qrc:/qml/automotive.qml"))
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
