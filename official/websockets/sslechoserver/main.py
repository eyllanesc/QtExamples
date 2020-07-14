import sys

from Qt.QtCore import QCoreApplication

import securesocketclient_rc  # noqa: F401
from sslechoserver import SslEchoServer


def main():

    app = QCoreApplication(sys.argv)

    server = SslEchoServer(1234)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
