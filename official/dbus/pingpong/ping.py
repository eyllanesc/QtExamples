from PyQt5.QtCore import QCoreApplication
from PyQt5.QtDBus import QDBusConnection, QDBusInterface, QDBusReply

from ping_common import SERVICE_NAME


def main():
    import sys

    app = QCoreApplication(sys.argv)  # noqa: F841

    if not QDBusConnection.sessionBus().isConnected():
        sys.stderr.write(
            "Cannot connect to the D-Bus session bus.\n"
            "To start it, run:\n"
            "\teval `dbus-launch --auto-syntax`\n"
        )
        sys.exit(1)

    iface = QDBusInterface(SERVICE_NAME, "/", "", QDBusConnection.sessionBus())

    if iface.isValid():
        msg = iface.call("ping", sys.argv[1] if len(sys.argv) > 1 else "")
        reply = QDBusReply(msg)

        if reply.isValid():
            sys.stdout.write("Reply was: %s\n" % reply.value())
            sys.exit()

        sys.stderr.write("Call failed: %s\n" % reply.error().message())
        sys.exit(1)

    sys.stderr.write("%s\n" % QDBusConnection.sessionBus().lastError().message())
    sys.exit(1)


if __name__ == "__main__":
    main()
