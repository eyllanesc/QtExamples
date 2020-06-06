from PyQt5.QtCore import QCoreApplication, Qt, QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView

import maroon_rc  # noqa: F401


def main():
    import sys

    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setOrganizationName("QtExamples")

    app = QGuiApplication(sys.argv)

    view = QQuickView()
    view.engine().quit.connect(app.quit)
    view.setSource(QUrl("qrc:/demos/maroon/maroon.qml"))
    if view.status() == QQuickView.Error:
        sys.exit(-1)
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    view.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
