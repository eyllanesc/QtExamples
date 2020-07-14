from Qt.QtCore import QCoreApplication, QPoint, Qt, QTimer, QUrl, Slot
from Qt.QtGui import QDesktopServices, QPixmap
from Qt.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from Qt.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
                          QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

import data_rc  # noqa: F401
import sip


class WebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.featurePermissionRequested.connect(self._handle_featurePermissionRequested)

    def acceptNavigationRequest(
        self,
        url: QUrl,
        navigation_type: QWebEnginePage.NavigationType,
        is_main_frame: bool,
    ) -> bool:
        if url.scheme() != "https":
            return True
        QDesktopServices.openUrl(url)
        return False

    def _handle_featurePermissionRequested(self, origin, feature):
        if feature != QWebEnginePage.Notifications:
            return
        self.setFeaturePermission(
            origin, feature, QWebEnginePage.PermissionGrantedByUser
        )


class NotificationPopup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.m_icon = QLabel()
        self.m_title = QLabel()
        self.m_message = QLabel()

        self.notification = None

        self.setWindowFlags(Qt.ToolTip)
        rootLayout = QHBoxLayout(self)

        rootLayout.addWidget(self.m_icon)

        bodyLayout = QVBoxLayout()
        rootLayout.addLayout(bodyLayout)

        titleLayout = QHBoxLayout()
        bodyLayout.addLayout(titleLayout)

        titleLayout.addWidget(self.m_title)
        titleLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding))

        close = QPushButton(self.tr("Close"))
        titleLayout.addWidget(close)
        close.clicked.connect(self.onClosed)

        bodyLayout.addWidget(self.m_message)
        self.adjustSize()

    def present(self, newNotification):
        if self.notification:
            self.notification.close()
            sip.delete(self.notification)
            self.notification = None

        self.notification = newNotification

        self.m_title.setText(f"<b>{self.notification.title()}</b>")
        self.m_message.setText(self.notification.message())
        self.m_icon.setPixmap(
            QPixmap.fromImage(self.notification.icon()).scaledToHeight(
                self.m_icon.height()
            )
        )

        self.show()
        self.notification.show()

        self.notification.closed.connect(self.onClosed)
        QTimer.singleShot(
            10000, lambda: self.onClosed() if self.notification is not None else None
        )

        # position our popup in the right corner of its parent widget
        self.move(
            self.parentWidget().mapToGlobal(
                self.parentWidget().rect().bottomRight()
                - QPoint(self.width() + 10, self.height() + 10)
            )
        )

    @Slot()
    def onClosed(self):
        self.hide()
        self.notification.close()
        self.notification = None

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.notification and event.button() == Qt.LeftButton:
            self.notification.click()
            self.onClosed()


def main():
    import sys

    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setOrganizationName("QtExamples")

    app = QApplication(sys.argv)

    view = QWebEngineView()

    # set custom page to open all page's links for https scheme in system browser
    view.setPage(WebEnginePage(view))

    profile = view.page().profile()
    popup = NotificationPopup(view)
    profile.setNotificationPresenter(popup.present)

    view.resize(640, 480)
    view.show()
    view.setUrl(QUrl("qrc:/index.html"))
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
