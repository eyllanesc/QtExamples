from Qt.QtGui import QGuiApplication
from Qt.QtWidgets import QApplication

from server import Server


def main():
    import sys

    app = QApplication(sys.argv)
    server = Server()
    QGuiApplication.setApplicationDisplayName(server.tr("Local Fortune Server"))
    server.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
