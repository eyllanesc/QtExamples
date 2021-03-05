from Qt.QtCore import QCoreApplication, Qt, QUrl, Slot
from Qt.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from Qt.QtWidgets import QApplication, QMainWindow, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_view = QWebEngineView()
        self.setCentralWidget(self.m_view)

        page = self.m_view.page()
        page.featurePermissionRequested.connect(self.on_featurePermissionRequested)
        page.load(QUrl("https://maps.google.com"))

    @Slot(QUrl, QWebEnginePage.Feature)
    def on_featurePermissionRequested(self, securityOrigin, feature):
        if feature != QWebEnginePage.Geolocation:
            return

        mgsbox = QMessageBox(self)
        mgsbox.setAttribute(Qt.WA_DeleteOnClose)
        mgsbox.setText(
            self.tr("{} wants to know your location".format(securityOrigin.host()))
        )
        mgsbox.setInformativeText(
            self.tr("Do you want to send your current location to this website?")
        )
        mgsbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        mgsbox.setDefaultButton(QMessageBox.Yes)

        page = self.m_view.page()

        if mgsbox.exec_() == QMessageBox.Yes:
            page.setFeaturePermission(
                securityOrigin, feature, QWebEnginePage.PermissionGrantedByUser
            )
        else:
            page.setFeaturePermission(
                securityOrigin, feature, QWebEnginePage.PermissionDeniedByUser
            )


def main():
    import sys

    QCoreApplication.setOrganizationName("QtExamples")
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)

    w = MainWindow()
    w.resize(1024, 768)
    w.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
