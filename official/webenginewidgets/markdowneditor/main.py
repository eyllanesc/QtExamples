from PyQt5.QtCore import (
    pyqtProperty,
    pyqtSignal,
    pyqtSlot,
    QCoreApplication,
    QDir,
    QFile,
    QIODevice,
    QObject,
    Qt,
    QTextStream,
    QUrl,
)
from PyQt5.QtGui import QDesktopServices, QFontDatabase
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox, QWidget
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel

from mainwindow_ui import Ui_MainWindow
import markdowneditor_rc  # noqa: F401


class Document(QObject):
    textChanged = pyqtSignal(str)

    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.m_text = ""

    def text(self):
        return self.m_text

    def setText(self, text):
        if text == self.m_text:
            return
        self.m_text = text
        self.textChanged.emit(text)

    text = pyqtProperty(str, fget=text, fset=setText, notify=textChanged)


class PreviewPage(QWebEnginePage):
    def acceptNavigationRequest(
        self, url: QUrl, _type: QWebEnginePage.NavigationType, isMainFrame: bool
    ) -> bool:
        if url.scheme() == "qrc":
            return True
        QDesktopServices.openUrl(url)
        return False


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setupUi(self)

        self.m_content = Document()
        self.m_filePath = ""

        self.editor.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        self.preview.setContextMenuPolicy(Qt.NoContextMenu)

        page = PreviewPage(self)
        self.preview.setPage(page)

        self.editor.textChanged.connect(
            lambda: self.m_content.setText(self.editor.toPlainText())
        )

        channel = QWebChannel(self)
        channel.registerObject("content", self.m_content)
        page.setWebChannel(channel)

        self.preview.setUrl(QUrl("qrc:/index.html"))

        self.actionNew.triggered.connect(self.onFileNew)
        self.actionOpen.triggered.connect(self.onFileOpen)
        self.actionSave.triggered.connect(self.onFileSave)
        self.actionSaveAs.triggered.connect(self.onFileSaveAs)
        self.actionExit.triggered.connect(self.onExit)

        self.editor.document().modificationChanged.connect(self.actionSave.setEnabled)

        defaultTextFile = QFile(":/default.md")
        defaultTextFile.open(QIODevice.ReadOnly)
        self.editor.setPlainText(defaultTextFile.readAll().data().decode())

    def openFile(self, path: str) -> None:
        f = QFile(path)

        if not f.open(QIODevice.ReadOnly):

            QMessageBox.warning(
                self,
                self.windowTitle(),
                self.tr(
                    "Could not open file %s: %s"
                    % (QDir.toNativeSeparators(path), f.errorString())
                ),
            )
            return

        self.m_filePath = path
        self.editor.setPlainText(f.readAll().data().decode())

    def isModified(self) -> bool:
        return self.editor.document().isModified()

    @pyqtSlot()
    def onFileNew(self):
        if self.isModified():
            button = QMessageBox.question(
                self,
                self.windowTitle(),
                self.tr(
                    "You have unsaved changes. Do you want to create a new document anyway?"
                ),
            )
            if button != QMessageBox.Yes:
                return

        self.m_filePath = ""
        self.editor.setPlainText(self.tr("## New document"))
        self.editor.document().setModified(False)

    @pyqtSlot()
    def onFileOpen(self):
        if self.isModified():
            button = QMessageBox.question(
                self,
                self.windowTitle(),
                self.tr(
                    "You have unsaved changes. Do you want to open a new document anyway?"
                ),
            )
            if button != QMessageBox.Yes:
                return

        path, _ = QFileDialog.getOpenFileName(
            self, self.tr("Open MarkDown File"), "", self.tr("MarkDown File (*.md)")
        )
        if not path:
            return

        self.openFile(path)

    @pyqtSlot()
    def onFileSave(self):
        if not self.m_filePath:
            self.onFileSaveAs()
            return

        f = QFile(self.m_filePath)
        if not f.open(QIODevice.WriteOnly | QIODevice.Text):
            QMessageBox.warning(
                self,
                self.windowTitle(),
                self.tr(
                    "Could not write to file %s: %s"
                    % (QDir.toNativeSeparators(self.m_filePath), f.errorString())
                ),
            )
            return

        text = QTextStream(f)
        text << self.editor.toPlainText()

        self.editor.document().setModified(False)

    @pyqtSlot()
    def onFileSaveAs(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            self.tr("Save MarkDown File"),
            "",
            self.tr("MarkDown File (*.md, *.markdown)"),
        )
        if not path:
            return
        self.m_filePath = path
        self.onFileSave()

    @pyqtSlot()
    def onExit(self):
        if self.isModified():
            button = QMessageBox.question(
                self,
                self.windowTitle(),
                self.tr("You have unsaved changes. Do you want to exit anyway?"),
            )
            if button != QMessageBox.Yes:
                return

        self.close()


def main():
    import sys

    QCoreApplication.setOrganizationName("QtExamples")
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
