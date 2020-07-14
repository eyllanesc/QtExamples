from Qt.QtCore import QCoreApplication, Qt, QUrl
from Qt.QtWebEngineWidgets import QWebEngineView
from Qt.QtWidgets import QApplication


def commandLineUrlArgument() -> QUrl:
    args = QCoreApplication.arguments()
    for arg in args[1:]:
        if not arg.startswith("_"):
            return QUrl.fromUserInput(arg)

    return QUrl("https://www.qt.io")


def main() -> None:
    import sys

    QCoreApplication.setOrganizationName("QtExamples")
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    view = QWebEngineView()
    view.setUrl(commandLineUrlArgument())
    view.resize(1024, 750)
    view.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
