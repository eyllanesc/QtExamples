from Qt.QtGui import QGuiApplication
from Qt.QtWidgets import QApplication

from client import Client


def main():
    import sys

    app = QApplication(sys.argv)
    client = Client()
    QGuiApplication.setApplicationDisplayName(client.tr("Local Fortune Client"))
    client.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
