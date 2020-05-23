from PyQt5.QtCore import pyqtSlot, QCoreApplication, QMetaObject, QObject
from PyQt5.QtDBus import QDBusConnection

from ping_common import SERVICE_NAME


class Pong(QObject):
    @pyqtSlot(str, result=str)
    def ping(self, arg):
        QMetaObject.invokeMethod(QCoreApplication.instance(), "quit")

        return 'ping("%s") got called' % arg


def main():
    import sys

    app = QCoreApplication(sys.argv)

    if not QDBusConnection.sessionBus().isConnected():
        sys.stderr.write(
            "Cannot connect to the D-Bus session bus.\n"
            "To start it, run:\n"
            "\teval `dbus-launch --auto-syntax`\n"
        )
        sys.exit(1)

    if not QDBusConnection.sessionBus().registerService(SERVICE_NAME):
        sys.stderr.write("%s\n" % QDBusConnection.sessionBus().lastError().message())
        sys.exit(1)

    pong = Pong()
    QDBusConnection.sessionBus().registerObject(
        "/", pong, QDBusConnection.ExportAllSlots
    )

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
