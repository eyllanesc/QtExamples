from PyQt5.QtCore import pyqtSlot, QCoreApplication, QFile, QIODevice, Qt, QUrl
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QLineEdit,
    QMainWindow,
    QSizePolicy,
    QStyle,
    QTextEdit,
)
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView

import jquery_rc  # noqa: F401


class MainWindow(QMainWindow):
    def __init__(self, url):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.progress = 0

        f = QFile()
        f.setFileName(":/jquery.min.js")
        f.open(QIODevice.ReadOnly)
        self.jQuery = f.readAll().data().decode()
        self.jQuery += "\nvar qt = { 'jQuery': jQuery.noConflict(true) };"
        f.close()

        self.view = QWebEngineView(self)
        self.view.load(url)

        self.view.loadFinished.connect(self.adjustLocation)
        self.view.titleChanged.connect(self.adjustTitle)
        self.view.loadProgress.connect(self.setProgress)
        self.view.loadFinished.connect(self.finishLoading)

        self.locationEdit = QLineEdit(self)
        self.locationEdit.setSizePolicy(
            QSizePolicy.Expanding, self.locationEdit.sizePolicy().verticalPolicy()
        )
        self.locationEdit.returnPressed.connect(self.changeLocation)

        toolBar = self.addToolBar(self.tr("Navigation"))
        toolBar.addAction(self.view.pageAction(QWebEnginePage.Back))
        toolBar.addAction(self.view.pageAction(QWebEnginePage.Forward))
        toolBar.addAction(self.view.pageAction(QWebEnginePage.Reload))
        toolBar.addAction(self.view.pageAction(QWebEnginePage.Stop))
        toolBar.addWidget(self.locationEdit)

        viewMenu = self.menuBar().addMenu(self.tr("&View"))
        viewSourceAction = QAction(self.tr("Page Source"), self)
        viewSourceAction.triggered.connect(self.viewSource)
        viewMenu.addAction(viewSourceAction)

        effectMenu = self.menuBar().addMenu(self.tr("&Effect"))
        effectMenu.addAction(self.tr("Highlight all links"), self.highlightAllLinks)

        self.rotateAction = QAction(self)
        self.rotateAction.setIcon(
            self.style().standardIcon(QStyle.SP_FileDialogDetailedView)
        )
        self.rotateAction.setCheckable(True)
        self.rotateAction.setText(self.tr("Turn images upside down"))
        self.rotateAction.toggled.connect(self.rotateImages)
        effectMenu.addAction(self.rotateAction)

        toolsMenu = self.menuBar().addMenu(self.tr("&Tools"))
        toolsMenu.addAction(self.tr("Remove GIF images"), self.removeGifImages)
        toolsMenu.addAction(
            self.tr("Remove all inline frames"), self.removeInlineFrames
        )
        toolsMenu.addAction(
            self.tr("Remove all object elements"), self.removeObjectElements
        )
        toolsMenu.addAction(
            self.tr("Remove all embedded elements"), self.removeEmbeddedElements
        )

        self.setCentralWidget(self.view)

    @pyqtSlot()
    def adjustLocation(self):
        self.locationEdit.setText(self.view.url().toString())

    @pyqtSlot()
    def changeLocation(self):
        url = QUrl.fromUserInput(self.locationEdit.text())
        self.view.load(url)
        self.view.setFocus()

    @pyqtSlot()
    def adjustTitle(self):
        if self.progress <= 0 or self.progress >= 100:
            self.setWindowTitle(self.view.title())
        else:
            self.setWindowTitle("%s (%2d)" % (self.view.title(), self.progress))

    @pyqtSlot(int)
    def setProgress(self, p):
        self.progress = p
        self.adjustTitle()

    @pyqtSlot()
    def finishLoading(self):
        self.progress = 100
        self.adjustTitle()
        self.view.page().runJavaScript(self.jQuery)
        self.rotateImages(self.rotateAction.isChecked())

    @pyqtSlot()
    def viewSource(self):
        self.textEdit = QTextEdit()
        self.textEdit.setAttribute(Qt.WA_DeleteOnClose)
        self.textEdit.adjustSize()
        self.textEdit.move(self.geometry().center() - self.textEdit.rect().center())
        self.textEdit.show()

        self.view.page().toHtml(self.textEdit.setPlainText)

    @pyqtSlot()
    def highlightAllLinks(self):
        code = "qt.jQuery('a').each( function () { qt.jQuery(this).css('background-color', 'yellow') } )"
        self.view.page().runJavaScript(code)

    @pyqtSlot(bool)
    def rotateImages(self, invert):
        code = ""
        if invert:
            code = "qt.jQuery('img').each( function () { qt.jQuery(this).css('transition', 'transform 2s'); qt.jQuery(this).css('transform', 'rotate(180deg)') } )"
        else:
            code = "qt.jQuery('img').each( function () { qt.jQuery(this).css('transition', 'transform 2s'); qt.jQuery(this).css('transform', 'rotate(0deg)') } )"
        self.view.page().runJavaScript(code)

    @pyqtSlot()
    def removeGifImages(self):
        code = "qt.jQuery('[src*=gif]').remove()"
        self.view.page().runJavaScript(code)

    @pyqtSlot()
    def removeInlineFrames(self):
        code = "qt.jQuery('iframe').remove()"
        self.view.page().runJavaScript(code)

    @pyqtSlot()
    def removeObjectElements(self):
        code = "qt.jQuery('object').remove()"
        self.view.page().runJavaScript(code)

    @pyqtSlot()
    def removeEmbeddedElements(self):
        code = "qt.jQuery('embed').remove()"
        self.view.page().runJavaScript(code)


def main():
    import sys

    QCoreApplication.setOrganizationName("QtExamples")
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    url = QUrl()

    if len(sys.argv) > 1:
        url = QUrl.fromUserInput(sys.argv[1])
    else:
        url = QUrl("http://www.google.com/ncr")

    browser = MainWindow(url)
    browser.resize(1024, 768)
    browser.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
