from PyQt5.QtCore import pyqtSlot, QByteArray, Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtNetwork import QAbstractSocket, QHostAddress, QTcpServer, QTcpSocket


TOTAL_BYTES = 50 * 1024 * 1024
PAYLOAD_SIZE = 64 * 1024  # 64 KB


class Dialog(QDialog):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.tcpServer = QTcpServer()
        self.tcpClient = QTcpSocket()
        self.tcpServerConnection: QTcpSocket = None

        self.bytesToWrite = 0
        self.bytesWritten = 0
        self.bytesReceived = 0

        self.clientProgressBar = QProgressBar()
        self.clientStatusLabel = QLabel(self.tr("Client ready"))
        self.serverProgressBar = QProgressBar()
        self.serverStatusLabel = QLabel(self.tr("Server ready"))

        self.startButton = QPushButton(self.tr("&Start"))
        self.quitButton = QPushButton(self.tr("&Quit"))

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(self.startButton, QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.quitButton, QDialogButtonBox.RejectRole)

        self.startButton.clicked.connect(self.start)
        self.quitButton.clicked.connect(self.close)
        self.tcpServer.newConnection.connect(self.acceptConnection)
        self.tcpClient.connected.connect(self.startTransfer)
        self.tcpClient.bytesWritten.connect(self.updateClientProgress)
        self.tcpClient.error.connect(self.displayError)

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.clientProgressBar)
        mainLayout.addWidget(self.clientStatusLabel)
        mainLayout.addWidget(self.serverProgressBar)
        mainLayout.addWidget(self.serverStatusLabel)
        mainLayout.addStretch(1)
        mainLayout.addSpacing(10)
        mainLayout.addWidget(self.buttonBox)

    @pyqtSlot()
    def start(self):
        self.startButton.setEnabled(False)

        QGuiApplication.setOverrideCursor(Qt.WaitCursor)

        self.bytesWritten = 0
        self.bytesReceived = 0

        while not self.tcpServer.isListening() and not self.tcpServer.listen():
            ret = QMessageBox.critical(
                self,
                self.tr("Loopback"),
                self.tr(
                    "Unable to start the test: %s" % (self.tcpServer.errorString())
                ),
                QMessageBox.Retry | QMessageBox.Cancel,
            )
            if ret == QMessageBox.Cancel:
                return

        self.serverStatusLabel.setText(self.tr("Listening"))
        self.clientStatusLabel.setText(self.tr("Connecting"))
        self.tcpClient.connectToHost(
            QHostAddress.LocalHost, self.tcpServer.serverPort()
        )

    @pyqtSlot()
    def acceptConnection(self):
        self.tcpServerConnection = self.tcpServer.nextPendingConnection()
        if not self.tcpServerConnection:
            self.serverStatusLabel.setText(
                self.tr("Error: got invalid pending connection!")
            )
            return

        self.tcpServerConnection.readyRead.connect(self.updateServerProgress)
        self.tcpServerConnection.error.connect(self.displayError)
        self.tcpServerConnection.disconnected.connect(
            self.tcpServerConnection.deleteLater
        )

        self.serverStatusLabel.setText(self.tr("Accepted connection"))
        self.tcpServer.close()

    @pyqtSlot()
    def startTransfer(self):
        # called when the TCP client connected to the loopback server
        self.bytesToWrite = TOTAL_BYTES - int(
            self.tcpClient.write(QByteArray(PAYLOAD_SIZE, "@"))
        )
        self.clientStatusLabel.setText(self.tr("Connected"))

    @pyqtSlot()
    def updateServerProgress(self):
        self.bytesReceived += int(self.tcpServerConnection.bytesAvailable())
        self.tcpServerConnection.readAll()

        self.serverProgressBar.setMaximum(TOTAL_BYTES)
        self.serverProgressBar.setValue(self.bytesReceived)
        self.serverStatusLabel.setText(
            self.tr("Received %dMB" % (self.bytesReceived / (1024 * 1024),))
        )

        if self.bytesReceived == TOTAL_BYTES:
            self.tcpServerConnection.close()
            self.startButton.setEnabled(True)

            QGuiApplication.restoreOverrideCursor()

    @pyqtSlot("qint64")
    def updateClientProgress(self, numBytes):
        self.bytesWritten += int(numBytes)

        if self.bytesToWrite > 0 and self.tcpClient.bytesToWrite() <= 4 * PAYLOAD_SIZE:
            self.bytesToWrite -= self.tcpClient.write(
                QByteArray(min(self.bytesToWrite, PAYLOAD_SIZE), "@")
            )

        self.clientProgressBar.setMaximum(TOTAL_BYTES)
        self.clientProgressBar.setValue(self.bytesWritten)
        self.clientStatusLabel.setText(
            self.tr("Sent %dMB" % (self.bytesWritten / (1024 * 1024),))
        )

    @pyqtSlot(QAbstractSocket.SocketError)
    def displayError(self, socketError):
        if socketError == QTcpSocket.RemoteHostClosedError:
            return

        QMessageBox.information(
            self,
            self.tr("Network error"),
            self.tr(
                "The following error occurred: %s." % (self.tcpClient.errorString(),)
            ),
        )
        self.tcpClient.close()
        self.tcpServer.close()
        self.clientProgressBar.reset()
        self.serverProgressBar.reset()
        self.clientStatusLabel.setText(self.tr("Client ready"))
        self.serverStatusLabel.setText(self.tr("Server ready"))
        self.startButton.setEnabled(True)
        QGuiApplication.restoreOverrideCursor()


def main() -> None:
    import sys

    app = QApplication(sys.argv)

    dialog = Dialog()
    dialog.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
