# -*- coding: utf-8 -*-
from Qt.QtWidgets import QApplication

from view import View


def main():
    import sys

    app = QApplication(sys.argv)

    w = View()
    w.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
