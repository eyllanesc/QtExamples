from PyQt5.QtWidgets import QApplication

from dialog import Dialog


def main():
    import sys

    app = QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
