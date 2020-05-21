from PyQt5.QtCore import QCoreApplication, Qt, QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

import resources_rc  # noqa: F401


def main():
    import os
    import sys

    QCoreApplication.setOrganizationName("QtExamples")
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QGuiApplication(sys.argv)

    os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"

    engine = QQmlApplicationEngine()

    isEmbedded = False

    engine.rootContext().setContextProperty("isEmbedded", isEmbedded)

    engine.load(QUrl("qrc:/qml/main.qml"))

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
