from PyQt5.QtCore import (
    pyqtSlot,
    QCoreApplication,
    QEventLoop,
    QObject,
    QPointF,
    Qt,
    QUrl,
)
from PyQt5.QtGui import QKeySequence, QPainter
from PyQt5.QtWidgets import QApplication, QDialog, QShortcut
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView

import data_rc  # noqa: F401


class PrintHandler(QObject):
    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent)
        self.m_page: QWebEnginePage = None
        self.m_inPrintPreview = False

    def setPage(self, page: QWebEnginePage) -> None:
        assert not self.m_page
        self.m_page = page
        self.m_page.printRequested.connect(self.printPreview)

    @pyqtSlot()
    def print(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self.m_page.view())
        if dialog.exec_() != QDialog.Accepted:
            return
        self.printDocument(printer)

    @pyqtSlot()
    def printPreview(self):
        if not self.m_page:
            return
        if self.m_inPrintPreview:
            return
        self.m_inPrintPreview = True
        printer = QPrinter()
        preview = QPrintPreviewDialog(printer, self.m_page.view())
        preview.paintRequested.connect(self.printDocument)
        preview.exec()
        self.m_inPrintPreview = False

    @pyqtSlot(QPrinter)
    def printDocument(self, printer):
        loop = QEventLoop()
        result = False

        def printPreview(success):
            nonlocal result
            result = success
            loop.quit()

        self.m_page.print(printer, printPreview)
        loop.exec_()
        if not result:
            painter = QPainter()
            if painter.begin(printer):
                font = painter.font()
                font.setPixelSize(20)
                painter.setFont(font)
                painter.drawText(QPointF(10, 25), "Could not generate print preview.")
                painter.end()


def main():
    import sys

    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    view = QWebEngineView()
    view.setUrl(QUrl("qrc:/index.html"))
    view.resize(1024, 750)
    view.show()

    handler = PrintHandler()
    handler.setPage(view.page())

    printPreviewShortCut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_P), view)
    printShortCut = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_P), view)

    printPreviewShortCut.activated.connect(handler.printPreview)
    printShortCut.activated.connect(handler.print)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
