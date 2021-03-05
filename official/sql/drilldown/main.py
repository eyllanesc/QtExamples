from Qt.QtWidgets import QApplication

from connection import createConnection
from view import View
import drilldown_rc  # noqa: F401


def main():
    import sys

    app = QApplication(sys.argv)

    if not createConnection():
        sys.exit(-1)

    view = View("items", "images")
    view.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
