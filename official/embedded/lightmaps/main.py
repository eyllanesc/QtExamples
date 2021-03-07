# -*- coding: utf-8 -*-
from Qt.QtWidgets import QApplication

from mapzoom import MapZoom


def main():
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName("LightMaps")

    w = MapZoom()
    w.resize(600, 450)
    w.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
