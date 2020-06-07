import ctypes
from PyQt5.QtCore import QSettings, Qt, QUrl
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine

import Fakequickcontrols2

import resources_rc  # noqa: F401

qtquickcontrols2 = ctypes.CDLL("libQt5QuickControls2.so.5")
qname = qtquickcontrols2._ZN11QQuickStyle4nameEv


def main():
    import sys

    QGuiApplication.setApplicationName("Gallery")
    QGuiApplication.setOrganizationName("QtProject")
    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QGuiApplication(sys.argv)

    QIcon.setThemeName("gallery")

    settings = QSettings()

    style = Fakequickcontrols2.name()
    if style:
        settings.setValue("style", style)
    else:
        Fakequickcontrols2.setStyle(settings.value("style"))

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty(
        "availableStyles", Fakequickcontrols2.availableStyles()
    )
    engine.load(QUrl("qrc:/gallery.qml"))
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
