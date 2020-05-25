from PySide2.QtCore import QByteArray, QCoreApplication, QFile, QIODevice, Qt, QUrl
from PySide2.QtWidgets import QApplication
from PySide2.QtWebEngineCore import (
    QWebEngineUrlRequestJob,
    QWebEngineUrlScheme,
    QWebEngineUrlSchemeHandler,
)
from PySide2.QtWebEngineWidgets import QWebEnginePage, QWebEngineProfile, QWebEngineView

import webui_rc  # noqa: F401

SCHEMENAME = "webui"


class WebUiHandler(QWebEngineUrlSchemeHandler):
    def requestStarted(self, job: QWebEngineUrlRequestJob) -> None:
        webUiOrigin = QUrl(SCHEMENAME + ":")
        GET: QByteArray = QByteArray(b"GET")
        POST: QByteArray = QByteArray(b"POST")

        method = job.requestMethod()
        url = job.requestUrl()
        initiator = job.initiator()
        if method == GET and url == WebUiHandler.aboutUrl:
            f = QFile(":/about.html", job)
            f.open(QIODevice.ReadOnly)
            job.reply(b"text/html", f)
        elif (
            method == POST and url == WebUiHandler.aboutUrl and initiator == webUiOrigin
        ):
            job.fail(QWebEngineUrlRequestJob.RequestAborted)
            QApplication.exit()
        else:
            job.fail(QWebEngineUrlRequestJob.UrlNotFound)

    @classmethod
    def registerUrlScheme(cls):
        webUiScheme = QWebEngineUrlScheme(cls.schemeName)
        webUiScheme.setFlags(
            QWebEngineUrlScheme.SecureScheme
            | QWebEngineUrlScheme.LocalScheme
            | QWebEngineUrlScheme.LocalAccessAllowed
        )
        QWebEngineUrlScheme.registerScheme(webUiScheme)

    schemeName: QByteArray = SCHEMENAME.encode()
    aboutUrl: QUrl = QUrl(SCHEMENAME + ":about")


def main():
    import sys

    QCoreApplication.setOrganizationName("QtExamples")
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    WebUiHandler.registerUrlScheme()

    app = QApplication(sys.argv)

    profile = QWebEngineProfile()
    handler = WebUiHandler()
    profile.installUrlSchemeHandler(WebUiHandler.schemeName, handler)

    page = QWebEnginePage(profile)
    page.load(WebUiHandler.aboutUrl)

    view = QWebEngineView()
    view.setPage(page)
    view.setContextMenuPolicy(Qt.NoContextMenu)
    view.resize(500, 600)
    view.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
