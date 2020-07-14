from Qt.QtCore import QCoreApplication, Qt, QUrl
from Qt.QtGui import QGuiApplication
from Qt.QtQml import QQmlApplicationEngine

import resources_rc  # noqa: F401


def main():
    import sys

    QCoreApplication.setOrganizationName("QtExamples")
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # QtWebEngine::initialize()

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load(QUrl("qrc:/WebBrowser.qml"))

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
