from PyQt5.QtWidgets import QApplication

from clientapplication import ClientApplication

import logfile_rc  # noqa: F401


def main():
    import sys

    app = QApplication(sys.argv)

    client = ClientApplication()
    client.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
