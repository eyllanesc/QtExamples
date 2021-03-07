# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication

from tablewidget import TableWidget


def main():
    import sys

    app = QApplication(sys.argv)

    w = TableWidget()
    w.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
