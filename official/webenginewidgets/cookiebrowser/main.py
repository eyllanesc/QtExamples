from functools import partial

from Qt.QtCore import QCoreApplication, QDateTime, Qt, QUrl, Signal, Slot
from Qt.QtGui import QColor
from Qt.QtNetwork import QNetworkCookie
from Qt.QtWebEngineCore import QWebEngineCookieStore
from Qt.QtWidgets import (QApplication, QDialog, QMainWindow, QSizePolicy,
                          QSpacerItem, QVBoxLayout, QWidget)

from cookiedialog_ui import Ui_CookieDialog
from cookiewidget_ui import Ui_CookieWidget
from mainwindow_ui import Ui_MainWindow


class CookieWidget(QWidget, Ui_CookieWidget):
    def __init__(self, cookie: QNetworkCookie, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAutoFillBackground(True)
        self.m_nameLabel.setText(cookie.name().data().decode())
        self.m_domainLabel.setText(cookie.domain())
        self.m_viewButton.clicked.connect(self.viewClicked)
        self.m_deleteButton.clicked.connect(self.deleteClicked)

    def setHighlighted(self, enabled: bool) -> None:
        p = self.palette()
        p.setColor(
            self.backgroundRole(), QColor(0xF0, 0xF8, 0xFF) if enabled else Qt.white
        )
        self.setPalette(p)

    deleteClicked = Signal()
    viewClicked = Signal()


class CookieDialog(QDialog, Ui_CookieDialog):
    def __init__(self, cookie: QNetworkCookie = None, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        if cookie:
            self.m_nameLineEdit.setText(cookie.name().data().decode())
            self.m_domainLineEdit.setText(cookie.domain())
            self.m_valueLineEdit.setText(cookie.value().data().decode())
            self.m_pathLineEdit.setText(cookie.path())
            self.m_dateEdit.setDate(cookie.expirationDate().date())
            self.m_isSecureComboBox.addItem(
                self.tr("yes") if cookie.isSecure() else self.tr("no")
            )
            self.m_isHttpOnlyComboBox.addItem(
                self.tr("yes") if cookie.isHttpOnly() else self.tr("no")
            )
            self.m_addButton.setVisible(False)
            self.m_cancelButton.setText(self.tr("Close"))

        else:
            self.m_nameLineEdit.setReadOnly(False)
            self.m_domainLineEdit.setReadOnly(False)
            self.m_valueLineEdit.setReadOnly(False)
            self.m_pathLineEdit.setReadOnly(False)
            self.m_dateEdit.setReadOnly(False)
            self.m_dateEdit.setDate(QDateTime.currentDateTime().addYears(1).date())
            self.m_isSecureComboBox.addItem(self.tr("no"))
            self.m_isSecureComboBox.addItem(self.tr("yes"))
            self.m_isHttpOnlyComboBox.addItem(self.tr("no"))
            self.m_isHttpOnlyComboBox.addItem(self.tr("yes"))

    def cookie(self):
        cookie = QNetworkCookie()
        cookie.setDomain(self.m_domainLineEdit.text())
        cookie.setName(self.m_nameLineEdit.text().encode())
        cookie.setValue(self.m_valueLineEdit.text().encode())
        cookie.setExpirationDate(QDateTime(self.m_dateEdit.date()))
        cookie.setPath(self.m_pathLineEdit.text())
        cookie.setSecure(self.m_isSecureComboBox.currentText() == self.tr("yes"))
        cookie.setHttpOnly(self.m_isHttpOnlyComboBox.currentText() == self.tr("yes"))
        return cookie


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, url: QUrl) -> None:
        super().__init__()
        self.setupUi(self)

        self.m_cookies = []

        self.m_urlLineEdit.setText(url.toString())

        self.m_layout = QVBoxLayout()
        self.m_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        self.m_layout.setContentsMargins(0, 0, 0, 0)
        self.m_layout.setSpacing(0)

        w = QWidget()
        p = w.palette()
        p.setColor(self.widget.backgroundRole(), Qt.white)
        w.setPalette(p)
        w.setLayout(self.m_layout)

        self.m_scrollArea.setWidget(w)
        self.m_scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.m_scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.m_urlButton.clicked.connect(self.handleUrlClicked)
        self.m_deleteAllButton.clicked.connect(self.handleDeleteAllClicked)
        self.m_newButton.clicked.connect(self.handleNewClicked)

        self.m_store: QWebEngineCookieStore = self.m_webview.page().profile().cookieStore()
        self.m_store.cookieAdded.connect(self.handleCookieAdded)
        self.m_store.loadAllCookies()
        self.m_webview.load(url)

    def containsCookie(self, cookie: QNetworkCookie):
        for c in self.m_cookies:
            if c.hasSameIdentifier(cookie):
                return True
        return False

    @Slot(QNetworkCookie)
    def handleCookieAdded(self, cookie: QNetworkCookie):
        if self.containsCookie(cookie):
            return

        widget = CookieWidget(cookie)
        widget.setHighlighted(len(self.m_cookies) % 2)

        self.m_cookies.append(QNetworkCookie(cookie))
        self.m_layout.insertWidget(0, widget)

        widget.deleteClicked.connect(
            partial(self._on_deleteClicked, QNetworkCookie(cookie), widget)
        )
        widget.viewClicked.connect(
            partial(self._on_viewClicked, QNetworkCookie(cookie))
        )

    def _on_deleteClicked(self, cookie: QNetworkCookie, widget: QWidget):
        self.m_store.deleteCookie(QNetworkCookie(cookie))
        # FIXME
        # sip.delete(widget)
        self.m_cookies.remove(cookie)
        for i in range(self.m_layout.count() - 1, -1, -1):
            w = self.m_layout.itemAt(i).widget()
            if isinstance(w, CookieWidget):
                w.setHighlighted(i % 2)

    def _on_viewClicked(self, cookie):
        dialog = CookieDialog(cookie)
        dialog.exec_()

    @Slot()
    def handleDeleteAllClicked(self):
        self.m_store.deleteAllCookies()
        for i in range(self.m_layout.count() - 1, -1, -1):
            w = self.m_layout.itemAt(i).widget()
            if w:
                sip.delete(w)
        self.m_cookies.clear()

    @Slot()
    def handleNewClicked(self):
        dialog = CookieDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.m_store.setCookie(QNetworkCookie(dialog.cookie()))

    @Slot()
    def handleUrlClicked(self):
        self.m_webview.load(QUrl.fromUserInput(self.m_urlLineEdit.text()))


def main():
    import sys

    QCoreApplication.setOrganizationName("QtExamples")
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    w = MainWindow(QUrl("http://qt.io"))
    w.resize(1024, 768)
    w.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
