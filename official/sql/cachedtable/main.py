from Qt.QtWidgets import QApplication

from connection import createConnection
from tableeditor import TableEditor


def main():
    import sys

    app = QApplication(sys.argv)
    if not createConnection():
        sys.exit(-1)

    editor = TableEditor("person")
    editor.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
