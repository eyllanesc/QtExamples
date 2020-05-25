import sys

from PyQt5.QtCore import (
    pyqtSlot,
    QCommandLineParser,
    QCoreApplication,
    QObject,
    QT_VERSION_STR,
    QUrl,
)
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEnginePage


class Html2PdfConverter(QObject):
    def __init__(self, inputPath: str, outputPath: str) -> None:
        super().__init__()
        self.m_inputPath = inputPath
        self.m_outputPath = outputPath
        self.m_page = QWebEnginePage()

        self.m_page.loadFinished.connect(self.loadFinished)
        self.m_page.pdfPrintingFinished.connect(self.pdfPrintingFinished)

    def run(self) -> bool:
        self.m_page.load(QUrl.fromUserInput(self.m_inputPath))
        return QApplication.exec_()

    @pyqtSlot(bool)
    def loadFinished(self, ok: bool):
        if not ok:
            sys.stderr.write("failed to load URL '%s'" % (self.m_inputPath,))
            QCoreApplication.exit(1)
            return
        self.m_page.printToPdf(self.m_outputPath)

    @pyqtSlot(str, bool)
    def pdfPrintingFinished(self, filePath: str, success: bool):
        if not success:
            sys.stderr.write("failed to print to output file '%s'" % (filePath,))
            QCoreApplication.exit(1)
        else:
            QCoreApplication.quit()


def main():
    app = QApplication(sys.argv)

    QCoreApplication.setOrganizationName("QtExamples")
    QCoreApplication.setApplicationName("html2pdf")
    QCoreApplication.setApplicationVersion(QT_VERSION_STR)

    parser = QCommandLineParser()
    parser.setApplicationDescription(
        QCoreApplication.translate(
            "main", "Converts the web page INPUT into the PDF file OUTPUT."
        )
    )
    parser.addHelpOption()
    parser.addVersionOption()
    parser.addPositionalArgument(
        QCoreApplication.translate("main", "INPUT"),
        QCoreApplication.translate("main", "Input URL for PDF conversion."),
    )
    parser.addPositionalArgument(
        QCoreApplication.translate("main", "OUTPUT"),
        QCoreApplication.translate("main", "Output file name for PDF conversion."),
    )

    parser.process(QCoreApplication.arguments())

    requiredArguments = parser.positionalArguments()
    if len(requiredArguments) != 2:
        parser.showHelp(1)

    converter = Html2PdfConverter(*requiredArguments[:2])
    ret = converter.run()
    sys.exit(ret)


if __name__ == "__main__":
    main()
