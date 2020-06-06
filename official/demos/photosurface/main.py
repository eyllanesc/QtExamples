from PyQt5.QtCore import (
    QCoreApplication,
    QCommandLineParser,
    QDir,
    QMimeDatabase,
    QStandardPaths,
    QT_VERSION_STR,
    QUrl,
)
from PyQt5.QtGui import QImageReader
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickWindow
from PyQt5.QtQml import QQmlApplicationEngine, QQmlContext

import photosurface_rc  # noqa: F401


def imageNameFilters():
    result = []
    mimeDatabase = QMimeDatabase()
    supportedMimeTypes = QImageReader.supportedMimeTypes()
    for m in supportedMimeTypes:
        suffixes = mimeDatabase.mimeTypeForName(m.data().decode()).suffixes()
        for suffix in suffixes:
            result.append(f"*.{suffix}")
    return result


def main():
    import sys

    app = QApplication(sys.argv)

    QQuickWindow.setDefaultAlphaBuffer(True)

    QCoreApplication.setApplicationName("Photosurface")
    QCoreApplication.setOrganizationName("QtProject")
    QCoreApplication.setApplicationVersion(QT_VERSION_STR)
    parser = QCommandLineParser()
    parser.setApplicationDescription("Qt Quick Demo - Photo Surface")
    parser.addHelpOption()
    parser.addVersionOption()
    parser.addPositionalArgument("directory", "The image directory or URL to show.")
    parser.process(app)

    initialUrl = QUrl()
    if parser.positionalArguments():
        initialUrl = QUrl.romUserInput(
            parser.positionalArguments()[0], QDir.currentPath(), QUrl.AssumeLocalFile
        )
        if not initialUrl.isValid():
            print(
                'Invalid argument: "',
                parser.positionalArguments()[0],
                '": ',
                initialUrl.errorString(),
            )
            sys.exit(1)

    nameFilters = imageNameFilters()

    engine = QQmlApplicationEngine()
    context: QQmlContext = engine.rootContext()

    picturesLocationUrl = QUrl.fromLocalFile(QDir.homePath())
    picturesLocations = QStandardPaths.standardLocations(
        QStandardPaths.PicturesLocation
    )
    if picturesLocations:
        picturesLocationUrl = QUrl.fromLocalFile(picturesLocations[0])
        if not initialUrl and QDir(picturesLocations[0]).entryInfoList(
            nameFilters, QDir.Files
        ):
            initialUrl = picturesLocationUrl

    context.setContextProperty("contextPicturesLocation", picturesLocationUrl)
    context.setContextProperty("contextInitialUrl", initialUrl)
    context.setContextProperty("contextImageNameFilters", nameFilters)

    engine.load(QUrl("qrc:///photosurface.qml"))
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
