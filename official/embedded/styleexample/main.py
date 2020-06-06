from PyQt5.QtWidgets import QApplication

from stylewidget import StyleWidget


def main():
    import sys

    app = QApplication(sys.argv)

    app.setApplicationName("style")
    app.setOrganizationName("QtProject")
    app.setOrganizationDomain("www.qt-project.org")

    widget = StyleWidget()
    widget.showFullScreen()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
