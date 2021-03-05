from Qt.QtCore import QCoreApplication, Qt, QTimer, QUrl
from Qt.QtGui import QGuiApplication
from Qt.QtNetwork import QNetworkProxy
from Qt.QtQml import QQmlApplicationEngine
from Qt.QtWidgets import QApplication

import customdialogs_rc  # noqa: F401
from server import Server

QT_NO_WIDGETS = True


def main():
    import sys

    QCoreApplication.setOrganizationName("QtExamples")
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # QtWebEngine::initialize()

    if QT_NO_WIDGETS:
        app = QApplication(sys.argv)
    else:
        app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    server = Server(engine)

    engine.load(QUrl("qrc:/main.qml"))
    QTimer.singleShot(0, server.run)

    proxy = QNetworkProxy()
    proxy.setType(QNetworkProxy.HttpProxy)
    proxy.setHostName("localhost")
    proxy.setPort(5555)
    QNetworkProxy.setApplicationProxy(proxy)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
